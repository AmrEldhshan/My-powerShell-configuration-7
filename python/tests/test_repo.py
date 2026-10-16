"""Repository-level tests for the Python tools.

These deliberately avoid importing the tool modules themselves, because they
pull in heavy optional dependencies (PyQt5, pyshark, yt-dlp, speedtest) and
several of them execute code at import time. Instead these tests assert
invariants about the repository layout that CI can verify on any platform.
"""

import pathlib
import py_compile
import sys

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
PYTHON_DIR = REPO_ROOT / "python"

TOOLS = sorted(PYTHON_DIR.glob("*.py"))
TOOLS = [tool for tool in TOOLS if tool.name != "__init__.py"]


def test_python_tools_directory_exists():
    assert PYTHON_DIR.is_dir(), "python/ directory is missing"


def test_repo_has_python_tools():
    assert TOOLS, "expected at least one Python tool in python/"


@pytest.mark.parametrize("tool", TOOLS, ids=lambda p: p.name)
def test_tool_filename_is_importable(tool):
    """Filenames with spaces cannot be imported and break every downstream tool."""
    assert " " not in tool.name, f"{tool.name} contains spaces and is not importable"
    assert tool.stem.isidentifier(), f"{tool.stem} is not a valid Python identifier"


@pytest.mark.parametrize("tool", TOOLS, ids=lambda p: p.name)
def test_tool_compiles(tool):
    """Every advertised tool must at minimum be valid Python."""
    py_compile.compile(str(tool), doraise=True)


@pytest.mark.parametrize("tool", TOOLS, ids=lambda p: p.name)
def test_tool_has_a_main_guard(tool):
    """Scripts meant to be run directly should guard their entry point."""
    source = tool.read_text(encoding="utf-8")
    assert "__main__" in source, f"{tool.name} has no `if __name__` main guard"


def test_readme_python_table_matches_disk():
    """The README must not advertise tools that do not exist."""
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    import re

    section = re.search(
        r"(?s)### .*Available Python Tools(.*?)\n### ", readme
    )
    assert section, "README is missing the 'Available Python Tools' section"

    documented = re.findall(r"\*\*`([^`]+\.py)`\*\*", section.group(1))
    assert documented, "README lists no Python tools"

    for name in documented:
        assert (PYTHON_DIR / name).is_file(), f"README documents missing file: {name}"


def test_readme_run_examples_reference_real_files():
    """Every `python <file>.py` snippet in the README must resolve."""
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    import re

    referenced = set(re.findall(r"python\s+\"?([A-Za-z0-9_]+\.py)\"?", readme))

    for name in referenced:
        assert (PYTHON_DIR / name).is_file(), f"README example runs missing file: {name}"


def test_repository_declares_license():
    license_file = REPO_ROOT / "LICENSE"
    assert license_file.is_file(), "LICENSE file is missing"
    assert "MIT" in license_file.read_text(encoding="utf-8")


def test_gitattributes_normalizes_line_endings():
    attributes = REPO_ROOT / ".gitattributes"
    assert attributes.is_file(), ".gitattributes is missing"
    assert "eol=lf" in attributes.read_text(encoding="utf-8")


def test_python_sources_use_lf_line_endings():
    """Guards against editors silently reintroducing CRLF churn."""
    for tool in TOOLS:
        raw = tool.read_bytes()
        assert b"\r\n" not in raw, f"{tool.name} contains CRLF line endings"


def test_scripts_have_shebang_or_are_marked_executable():
    """POSIX-friendly entry points should be runnable via ./tool.py."""
    for tool in TOOLS:
        raw = tool.read_bytes()
        assert raw.startswith(b"#!"), f"{tool.name} is executable but has no shebang"


def test_python_version_floor():
    """The CI matrix targets 3.10+; keep the syntax compatible."""
    assert sys.version_info >= (3, 10)
