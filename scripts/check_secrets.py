#!/usr/bin/env python3
"""Run pinned Gitleaks scans without exposing scanner output."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PINNED_VERSION = "8.30.1"
HISTORY_LOG_OPTIONS = "--all --full-history --text --no-textconv --no-ext-diff"
DEFAULT_CONFIG = "[extend]\nuseDefault = true\n"


def _clean_environment(home: Path, temp: Path) -> dict[str, str]:
    return {
        "HOME": str(home),
        "PATH": "/usr/bin:/bin",
        "TMPDIR": str(temp),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
    }


def _has_symlink(root: Path, include_git: bool) -> bool:
    for current, directories, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        if not include_git and current_path == root and ".git" in directories:
            directories.remove(".git")
        for name in (*directories, *files):
            if (current_path / name).is_symlink():
                return True
    return False


def _copy_working_tree(source: Path, destination: Path) -> bool:
    if not source.is_dir() or _has_symlink(source, include_git=False):
        return False

    def ignored(directory: str, names: list[str]) -> set[str]:
        if Path(directory) == source:
            return {".git"} if ".git" in names else set()
        return set()

    try:
        shutil.copytree(source, destination, ignore=ignored, symlinks=True)
        # Rename repository controls so their contents are scanned, not loaded.
        for name in (".gitleaks.toml", ".gitleaksignore"):
            control = destination / name
            if control.exists():
                renamed = destination / (name + ".scan-input")
                if not control.is_file() or renamed.exists():
                    return False
                control.rename(renamed)
    except (OSError, shutil.Error):
        return False
    return True


def _copy_history(source: Path, destination: Path, env: dict[str, str]) -> bool:
    if not source.is_dir() or _has_symlink(source, include_git=True):
        return False
    try:
        result = subprocess.run(
            ["git", "clone", "--mirror", "--no-local", "--quiet", str(source), str(destination)],
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=120,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return result.returncode == 0


def _pinned_binary(binary: Path, env: dict[str, str]) -> bool:
    if not binary.is_file() or not os.access(binary, os.X_OK):
        return False
    try:
        result = subprocess.run(
            [str(binary), "version"],
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return result.returncode == 0 and result.stdout.strip().decode("ascii", "ignore") == PINNED_VERSION


def scan(root: Path, mode: str, binary: str | Path | None = None) -> str:
    """Return pass, finding, or error; never return scanner-provided text."""
    if mode not in {"working-tree", "history"}:
        return "error"
    configured_binary = binary if binary is not None else os.environ.get("GITLEAKS_BINARY")
    if not configured_binary:
        return "error"
    executable = Path(configured_binary).expanduser().absolute()
    try:
        source = root.resolve(strict=True)
        with tempfile.TemporaryDirectory(prefix="docs-ci-secrets-", dir=os.environ.get("TMPDIR")) as temp_name:
            temp = Path(temp_name)
            if temp == source or source in temp.parents:
                return "error"
            home = temp / "home"
            home.mkdir()
            env = _clean_environment(home, temp)
            if not _pinned_binary(executable, env):
                return "error"

            config = temp / "gitleaks.toml"
            config.write_text(DEFAULT_CONFIG, encoding="ascii")
            ignore_file = temp / "empty-ignore"
            ignore_file.write_bytes(b"")
            target = temp / "source"
            if mode == "working-tree":
                if not _copy_working_tree(source, target):
                    return "error"
                command = [str(executable), "dir", "--config", str(config)]
            else:
                if not _copy_history(source, target, env):
                    return "error"
                command = [str(executable), "git", "--config", str(config)]

            command.extend(
                [
                    "--gitleaks-ignore-path",
                    str(ignore_file),
                    "--ignore-gitleaks-allow",
                    "--exit-code",
                    "3",
                    "--no-banner",
                    "--redact=100",
                ]
            )
            if mode == "history":
                command.extend(["--log-opts=" + HISTORY_LOG_OPTIONS])
            command.append(str(target))
            try:
                result = subprocess.run(
                    command,
                    cwd=temp,
                    env=env,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                    timeout=180,
                )
            except (OSError, subprocess.SubprocessError):
                return "error"
            if result.returncode == 0:
                return "pass"
            if result.returncode == 3:
                return "finding"
            return "error"
    except (OSError, ValueError, subprocess.SubprocessError):
        return "error"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan working-tree files and Git history with Gitleaks 8.30.1")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--working-tree", action="store_true", help="scan current working-tree files")
    modes.add_argument("--history", action="store_true", help="scan all locally fetched Git history")
    args = parser.parse_args(argv)
    selected = ["working-tree"] if args.working_tree else ["history"] if args.history else ["working-tree", "history"]
    failed = False
    for mode in selected:
        result = scan(REPO_ROOT, mode)
        if result == "pass":
            status = "PASS"
        elif result == "finding":
            status = "FAIL (finding)"
            failed = True
        else:
            status = "ERROR (scanner unavailable or failed)"
            failed = True
        print(f"Secret scan ({mode}): {status}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
