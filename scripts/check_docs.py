#!/usr/bin/env python3
"""Validate the repository's documented Markdown subset."""

from __future__ import annotations

import argparse
import ipaddress
import os
import posixpath
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

REPO_ROOT = Path(__file__).resolve().parents[1]
CORPUS_ROOT = Path("blueprints")
PLACEHOLDERS = {"<repo-root>", "<config-dir>", "<report-dir>"}
RECIPE_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*\.md$")
ENTITY_RE = re.compile(r"&(?:[A-Za-z][A-Za-z0-9]*|#(?:[0-9]+|[xX][0-9A-Fa-f]+));")
ANGLE_RE = re.compile(r"<([^<>\r\n]*)>")
INLINE_LINK_RE = re.compile(r"(!?)\[([^\[\]\n]+)\]\((<[^<>\s]+>|[^()\s]+)\)")
REFERENCE_LINK_RE = re.compile(r"(!?)\[([^\[\]\n]+)\]\[([^\[\]\n]*)\]")
REFERENCE_DEF_RE = re.compile(r"^ {0,3}\[([^\[\]\n]+)\]:[ \t]*(<[^<>\s]+>|[^\s]+)[ \t]*$")
DOUBLE_ENCODING_RE = re.compile(r"%[0-9A-Fa-f]{2}")
BARE_LINK_RE = re.compile(r"(?i)(?<![a-z0-9])(?:[a-z][a-z0-9+.-]*://|www\.|(?:mailto|file|xmpp):)\S+")
REQUIRED_RECIPE_HEADINGS = (
    "Purpose",
    "Inputs",
    "Flow",
    "Boundaries",
    "Outputs",
    "Adaptation",
    "Verification",
)


def _ascii_markdown(raw: bytes) -> str:
    text = raw.decode("utf-8")
    if any(ord(char) not in (9, 10) and not 32 <= ord(char) <= 126 for char in text):
        raise ValueError("unsupported Markdown character")
    return text


def _mask_code(text: str) -> tuple[str, bool]:
    chars = list(text)
    offset = 0
    in_fence: tuple[str, int] | None = None
    for line in text.splitlines(keepends=True):
        body = line.rstrip("\n")
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", body)
        if in_fence is None and match:
            marker = match.group(1)
            if marker[0] == "`" and "`" in match.group(2):
                return "".join(chars), False
            in_fence = (marker[0], len(marker))
        elif in_fence is not None:
            marker, length = in_fence
            if re.match(rf"^ {{0,3}}{re.escape(marker)}{{{length},}}[ \t]*$", body):
                in_fence = None
        if in_fence is not None or match:
            for index in range(offset, offset + len(line)):
                if chars[index] != "\n":
                    chars[index] = " "
        offset += len(line)
    if in_fence is not None:
        return "".join(chars), False

    masked = "".join(chars)
    chars = list(masked)
    index = 0
    while index < len(chars):
        if chars[index] != "`":
            index += 1
            continue
        if index > 0 and chars[index - 1] == "\\":
            return "".join(chars), False
        end = index + 1
        while end < len(chars) and chars[end] == "`":
            end += 1
        delimiter = masked[index:end]
        closing = end
        while True:
            closing = masked.find(delimiter, closing)
            if closing < 0:
                break
            run_end = closing + len(delimiter)
            if (closing == 0 or masked[closing - 1] != "`") and (
                run_end == len(masked) or masked[run_end] != "`"
            ):
                break
            closing = run_end
        if closing < 0:
            return "".join(chars), False
        for position in range(index, closing + len(delimiter)):
            if chars[position] != "\n":
                chars[position] = " "
        index = closing + len(delimiter)
    return "".join(chars), True


def _valid_https_target(target: str) -> bool:
    if "\\" in target or any(ord(char) < 33 or ord(char) > 126 for char in target):
        return False
    try:
        raw_parts = urlsplit(target)
        if "%" in raw_parts.netloc or re.search(r"%(?![0-9A-Fa-f]{2})", target):
            return False
        decoded = unquote(target, errors="strict")
        if any(ord(char) < 33 or ord(char) > 126 for char in decoded) or DOUBLE_ENCODING_RE.search(decoded):
            return False
        parsed = urlsplit(decoded)
        host = parsed.hostname
        port = parsed.port
        if (
            parsed.scheme.casefold() != "https"
            or not parsed.netloc
            or "@" in parsed.netloc
            or host is None
            or port not in (None, 443)
            or host.endswith(".")
        ):
            return False
        host = host.casefold()
        try:
            ipaddress.ip_address(host)
            return False
        except ValueError:
            pass
        if host == "localhost" or host.endswith(
            (".localhost", ".local", ".internal", ".lan", ".test", ".invalid", ".example", ".onion", ".arpa")
        ):
            return False
        labels = host.split(".")
        return len(labels) >= 2 and bool(re.search(r"[a-z]", labels[-1])) and all(
            re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label) for label in labels
        )
    except (UnicodeDecodeError, ValueError):
        return False


def _link_target_is_safe(target: str, files: set[str], document: str) -> bool:
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    if target.startswith("https://"):
        return _valid_https_target(target)
    if (
        not target
        or "%" in target
        or target.startswith(("/", "~", "\\"))
        or "\\" in target
        or any(ord(char) < 33 or ord(char) > 126 for char in target)
    ):
        return False
    try:
        if re.search(r"%(?![0-9A-Fa-f]{2})", target):
            return False
        decoded = unquote(target, errors="strict")
        if any(ord(char) < 33 or ord(char) > 126 for char in decoded) or DOUBLE_ENCODING_RE.search(decoded):
            return False
        parsed = urlsplit(decoded)
    except (UnicodeDecodeError, ValueError):
        return False
    # Local anchors are outside the supported file-link subset: do not
    # report an unchecked fragment as a verified link.
    if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment:
        return False
    if not parsed.path:
        return False
    if parsed.path.startswith(("/", "~")) or "\\" in parsed.path:
        return False
    normalized = posixpath.normpath(posixpath.join(posixpath.dirname(document), parsed.path))
    if normalized.startswith("/") or normalized == ".." or normalized.startswith("../"):
        return False
    return normalized in files


def _validate_links(markdown: str, files: set[str], document: str) -> int:
    masked, valid_code = _mask_code(markdown)
    if not valid_code:
        return 1
    errors = sum(1 for _ in ENTITY_RE.finditer(masked))
    protected: list[tuple[int, int]] = []
    targets: list[str] = []
    definitions: dict[str, str] = {}
    offset = 0
    for line in masked.splitlines(keepends=True):
        body = line.rstrip("\n")
        definition = REFERENCE_DEF_RE.fullmatch(body)
        if definition:
            reference = " ".join(definition.group(1).casefold().split())
            if reference in definitions:
                errors += 1
            definitions[reference] = definition.group(2)
            targets.append(definition.group(2))
            protected.append((offset, offset + len(body)))
        elif re.match(r"^ {0,3}\[[^\]\n]+\]:", body):
            errors += 1
            protected.append((offset, offset + len(body)))
        offset += len(line)

    chars = list(masked)
    for start, end in protected:
        for index in range(start, end):
            if chars[index] != "\n":
                chars[index] = " "
    without_definitions = "".join(chars)
    link_matches: list[tuple[int, int]] = []
    for pattern in (INLINE_LINK_RE, REFERENCE_LINK_RE):
        for match in pattern.finditer(without_definitions):
            if any(match.start() < end and match.end() > start for start, end in link_matches):
                continue
            link_matches.append((match.start(), match.end()))
            if pattern is INLINE_LINK_RE:
                targets.append(match.group(3))
            else:
                reference = match.group(3) or match.group(2)
                key = " ".join(reference.casefold().split())
                if key not in definitions:
                    errors += 1
                else:
                    targets.append(definitions[key])

    chars = list(without_definitions)
    for start, end in link_matches:
        for index in range(start, end):
            if chars[index] != "\n":
                chars[index] = " "
    remaining = "".join(chars)
    if "[" in remaining or "]" in remaining:
        errors += 1

    for match in ANGLE_RE.finditer(masked):
        value = match.group(1)
        if f"<{value}>" in PLACEHOLDERS:
            continue
        if value.startswith("https://"):
            targets.append(value)
        else:
            errors += 1
    stripped_angles = ANGLE_RE.sub("", masked)
    if "<" in stripped_angles or ">" in stripped_angles:
        errors += 1
    bare_text = ANGLE_RE.sub("", remaining)
    if "@" in bare_text:
        errors += 1
    for match in BARE_LINK_RE.finditer(bare_text):
        targets.append(match.group(0))
    for target in targets:
        if not _link_target_is_safe(target, files, document):
            errors += 1
    return errors


def _is_frontmatter(text: str) -> bool:
    return bool(text.splitlines() and text.splitlines()[0].strip() == "---")


def _raise_walk_error(error: OSError) -> None:
    raise error


def _validate_recipe_headings(text: str) -> bool:
    headings = [match.group(1) for match in re.finditer(r"^## ([^\n]+)$", text, re.MULTILINE)]
    return tuple(headings) == REQUIRED_RECIPE_HEADINGS


def _walk_repository(root: Path) -> tuple[set[str], bool]:
    files: set[str] = set()
    safe = True
    for current, directories, names in os.walk(root, topdown=True, followlinks=False, onerror=_raise_walk_error):
        current_path = Path(current)
        if current_path == root and ".git" in directories:
            directories.remove(".git")
        for name in list(directories):
            path = current_path / name
            if path.is_symlink():
                directories.remove(name)
            elif not path.is_dir():
                safe = False
                directories.remove(name)
        for name in names:
            if current_path == root and name == ".git":
                continue
            path = current_path / name
            relative = path.relative_to(root).as_posix()
            if not path.is_symlink() and path.is_file():
                files.add(relative)
            elif not path.is_symlink():
                safe = False
    return files, safe


def _tracked_symlinks(root: Path) -> tuple[set[str], bool]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "--stage", "-z"],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=15,
        )
    except (OSError, subprocess.SubprocessError):
        return set(), False
    if result.returncode != 0:
        return set(), False
    symlinks: set[str] = set()
    for entry in result.stdout.split(b"\0"):
        if not entry:
            continue
        metadata, separator, path = entry.partition(b"\t")
        if not separator:
            return set(), False
        mode = metadata.split(b" ", 1)[0]
        if mode == b"120000":
            symlinks.add(os.fsdecode(path))
    return symlinks, True


def _corpus_files(corpus: Path) -> tuple[dict[str, str], set[str], set[str], bool]:
    documents: dict[str, str] = {}
    symlinks: set[str] = set()
    directories: set[str] = set()
    safe = True
    if corpus.is_symlink() or not corpus.is_dir():
        return documents, symlinks, directories, False
    for current, child_directories, names in os.walk(
        corpus, topdown=True, followlinks=False, onerror=_raise_walk_error
    ):
        current_path = Path(current)
        for name in list(child_directories):
            path = current_path / name
            relative = path.relative_to(corpus).as_posix()
            if path.is_symlink():
                symlinks.add(relative)
                child_directories.remove(name)
            elif path.is_dir():
                directories.add(relative)
            else:
                safe = False
                child_directories.remove(name)
        for name in names:
            path = current_path / name
            relative = path.relative_to(corpus).as_posix()
            if path.is_symlink():
                symlinks.add(relative)
            elif path.is_file() and path.suffix.casefold() == ".md":
                try:
                    documents[relative] = _ascii_markdown(path.read_bytes())
                except (OSError, UnicodeError, ValueError):
                    safe = False
            else:
                safe = False
    return documents, symlinks, directories, safe


def _valid_layout(documents: dict[str, str], directories: set[str]) -> bool:
    expected_directories = {"skills", "automations"}
    if directories != expected_directories or "README.md" not in documents:
        return False
    recipes = set(documents) - {"README.md"}
    if not recipes or not any(path.startswith("skills/") for path in recipes):
        return False
    if not any(path.startswith("automations/") for path in recipes):
        return False
    folded: set[str] = set()
    for path in documents:
        if path.casefold() in folded:
            return False
        folded.add(path.casefold())
        if path == "README.md":
            continue
        parts = path.split("/")
        if len(parts) != 2 or parts[0] not in expected_directories or not RECIPE_NAME_RE.fullmatch(parts[1]):
            return False
    return True


def _catalog_coverage(catalog: str, recipe_paths: set[str]) -> bool:
    masked, valid_code = _mask_code(catalog)
    if not valid_code:
        return False
    definitions: dict[str, str] = {}
    protected: list[tuple[int, int]] = []
    targets: list[str] = []
    offset = 0
    for line in masked.splitlines(keepends=True):
        body = line.rstrip("\n")
        definition = REFERENCE_DEF_RE.fullmatch(body)
        if definition:
            key = " ".join(definition.group(1).casefold().split())
            definitions[key] = definition.group(2)
            protected.append((offset, offset + len(body)))
        offset += len(line)
    chars = list(masked)
    for start, end in protected:
        for index in range(start, end):
            if chars[index] != "\n":
                chars[index] = " "
    remaining = "".join(chars)
    targets.extend(match.group(3) for match in INLINE_LINK_RE.finditer(remaining) if not match.group(1))
    for match in REFERENCE_LINK_RE.finditer(remaining):
        if match.group(1):
            continue
        key = " ".join((match.group(3) or match.group(2)).casefold().split())
        if key in definitions:
            targets.append(definitions[key])

    linked: set[str] = set()
    for target in targets:
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        normalized = posixpath.normpath(posixpath.join(".", parsed.path))
        linked.add(normalized)
    return recipe_paths.issubset(linked)


def _validate_repository(root: Path) -> bool:
    root = root.resolve()
    if not root.is_dir():
        return False
    tracked_links, git_ok = _tracked_symlinks(root)
    if not git_ok or tracked_links:
        return False
    all_files, tree_safe = _walk_repository(root)
    if not tree_safe:
        return False

    readme_path = root / "README.md"
    if readme_path.is_symlink() or not readme_path.is_file():
        return False
    try:
        readme = _ascii_markdown(readme_path.read_bytes())
    except (OSError, UnicodeError, ValueError):
        return False
    if _is_frontmatter(readme) or _validate_links(readme, all_files, "README.md"):
        return False
    corpus = root / CORPUS_ROOT
    documents, corpus_symlinks, corpus_directories, corpus_safe = _corpus_files(corpus)
    if not corpus_safe or corpus_symlinks or not _valid_layout(documents, corpus_directories):
        return False
    corpus_paths = set(documents)
    recipe_paths = corpus_paths - {"README.md"}
    catalog = documents["README.md"]
    if _is_frontmatter(catalog) or _validate_links(catalog, corpus_paths, "README.md"):
        return False
    if not _catalog_coverage(catalog, recipe_paths):
        return False
    for relative, text in documents.items():
        if _is_frontmatter(text):
            return False
        masked, valid_code = _mask_code(text)
        if not valid_code:
            return False
        if relative != "README.md" and not _validate_recipe_headings(masked):
            return False
        if _validate_links(text, corpus_paths, relative):
            return False
        # A symlink at any component of a local link target is excluded from
        # the regular-file set above, so it cannot satisfy a target lookup.
    return True


def validate_repository(root: Path = REPO_ROOT) -> bool:
    try:
        return _validate_repository(root)
    except (OSError, ValueError, UnicodeError, subprocess.SubprocessError):
        return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate repository Markdown structure and local links")
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    passed = validate_repository(args.root)
    print("Documentation validation: " + ("PASS" if passed else "FAIL"))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
