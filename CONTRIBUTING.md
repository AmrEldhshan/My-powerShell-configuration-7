# Contributing

Thanks for helping improve this PowerShell configuration. This document covers
how to get set up, what CI checks, and the conventions the project follows.

## Getting started

```powershell
git clone https://github.com/Amr-Khaled-Ahmed/My-powerShell-configuration-7.git
cd My-powerShell-configuration-7
```

You do not need to install this as your profile to contribute. The test suite
parses `Profile.ps1` rather than executing it, so a clean checkout is enough.

## Running the checks locally

### PowerShell

```powershell
Install-Module Pester -Scope CurrentUser -Force -SkipPublisherCheck
Install-Module PSScriptAnalyzer -Scope CurrentUser -Force

Invoke-Pester ./tests
Invoke-ScriptAnalyzer -Path ./Profile.ps1 -Severity Error
```

### Python

```powershell
pip install ruff pytest

ruff check python
pytest python/tests -v
```

## What CI enforces

| Workflow | Check | Purpose |
|----------|-------|---------|
| `powershell.yml` | Pester | Profile parses; README does not drift from the code |
| `powershell.yml` | PSScriptAnalyzer | No parse-level errors in `Profile.ps1` |
| `python.yml` | Ruff | Correctness and import hygiene in `python/` |
| `python.yml` | `compileall` | Every advertised script is valid Python |
| `python.yml` | pytest | Repository invariants hold |

## Conventions

### Line endings

`.gitattributes` forces LF in the repository and in every working tree. If your
editor keeps rewriting files to CRLF, that is a real problem here: it makes
every file show as fully modified. Turn off automatic CRLF conversion in your
editor rather than committing CRLF changes.

### Adding a PowerShell function

1. Add the function to `Profile.ps1`.
2. If it is user-facing, add a row to the matching table in the
   **Functions & Aliases** section of `README.md`.
3. Add it to the built-in `help-menu` list if it is a headline command.

The README table is verified by tests. Documenting a command that does not
exist, or renaming a function without updating the README, will fail CI.

### Startup performance

The profile is loaded on every shell, so keep the startup path cheap:

- Do not spawn external processes (Python, `git`, `winget`, ...) at load time.
- Use `Write-ZeroAccessDetail` for optional startup chatter so it only appears
  with `ZEROACCESS_VERBOSE=1`.
- Import modules directly; do not add `Get-Module -ListAvailable` probes to the
  startup path.
- Cache expensive generated scripts under `~/.config/zeroaccess/cache`.
- Verify with `pstats` (or `Measure-Command { . $PROFILE }`) before and after.

### Adding a Python tool

1. Add `python/<tool_name>.py`. Use `snake_case`; spaces in filenames break
   imports and are rejected by the test suite.
2. Start the file with `#!/usr/bin/env python3`.
3. Guard the entry point with `if __name__ == "__main__":`.
4. Add the file to the **Available Python Tools** table in `README.md`.
5. Keep it compiling under `python -m compileall python`.

Heavy third-party dependencies (PyQt5, pyshark, yt-dlp, speedtest) are not
installed in CI, so the tests never import the tools. If you add an import of a
new dependency, note it in the README prerequisites.

### Scope of changes

`Profile.ps1` is a single, large, user-facing file that people dot-source as
their daily shell. Changes to it should be additive and self-contained; avoid
restructuring or reformatting unrelated parts, and avoid renames of existing
functions without a strong reason.

## Reporting bugs

Include your PowerShell version (`$PSVersionTable.PSVersion`), OS, and the
exact command that failed along with its output.

## License

By contributing you agree that your contributions are licensed under the
[MIT License](LICENSE).