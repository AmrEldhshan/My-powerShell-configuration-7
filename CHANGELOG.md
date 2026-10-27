# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Fast-startup mode: cached Oh My Posh init script, direct module imports, and a
  pure-PowerShell banner instead of spawning Python/pyfiglet on every launch.
- Startup switches: `ZEROACCESS_QUIET`, `ZEROACCESS_VERBOSE`,
  `ZEROACCESS_CLEAR`, `ZEROACCESS_NO_OMP`, and `ZEROACCESS_EXTRA_MODULES`.
- `Reload-Profile` (`reload`), `Edit-Profile` (`ep`), `Get-ProfileStats`
  (`pstats`), and `mkcd` (`mcd`) helpers.
- Theme choice is persisted to `~/.config/zeroaccess/theme.txt`, and
  `$env:POSH_THEME` is now honoured on startup.
- `Start-SystemMaintenance -Repair` opt-in switch for `chkdsk`.
- `Watch-Performance -Count` for bounded sampling.
- `LICENSE` file containing the MIT license the README advertises.
- `.gitattributes` forcing LF line endings for all text files.
- `.gitignore` covering Python caches, virtual environments, editor state, and logs.
- GitHub Actions CI in two workflows:
  - `powershell.yml` runs Pester tests and PSScriptAnalyzer.
  - `python.yml` runs Ruff, byte-compilation, and pytest.
- Pester suite in `tests/Profile.Tests.ps1` covering profile parsing, structure
  invariants, README accuracy, and repository hygiene.
- pytest suite in `python/tests/test_repo.py` covering importable filenames,
  script compilation, entry-point guards, and README-to-disk consistency.
- `ruff.toml` pinning the lint rule set so results do not drift between Ruff releases.
- `CONTRIBUTING.md` documenting setup, local checks, and conventions.
- `CHANGELOG.md`.
- `python/requirements.txt` listing the optional dependencies for the Python tools.

### Changed

- The screen is no longer cleared on every shell launch; use
  `ZEROACCESS_CLEAR=1` to restore the old behaviour.
- Per-module startup output is hidden unless `ZEROACCESS_VERBOSE=1` is set.
- `PSGitHub` is opt-in via `ZEROACCESS_EXTRA_MODULES=1` to keep startup fast.
- README installation now points at the real `Profile.ps1` file.

### Fixed

- Theme switching no longer corrupts `$PROFILE`; the selected theme is stored
  in a small state file and is actually used on the next launch.
- `Find-InFile` builds paths with `-Filter` instead of Windows-only `\*.ext`
  strings, so it works on Linux and macOS.
- `venv` detects `python`/`python3`, uses the correct `Scripts`/`bin` activation
  path, and activates even when the environment already exists.
- `Test-NetworkSpeed` no longer calls the invalid
  `Invoke-RestMethod ... -OutFile` combination; it uses `speedtest`, `curl`, or
  a timed `Invoke-WebRequest` fallback.
- `Watch-Performance -Export` now runs in a `finally` block instead of being
  unreachable after an infinite loop.
- `Start-SystemMaintenance` no longer runs destructive `chkdsk /f /r` on every
  drive by default.
- Removed the hardcoded SSH secret from `my-hack-server`; set
  `SEGFAULT_SECRET` instead.
- `ssh-keygen`, `Get-PathEnvironment`, `Compare-Directories`,
  `Set-TerminalBackground`, and `New-TerminalProfile` are now cross-platform
  and/or guard missing Windows-only resources.
- `Measure-CodeQuality` checks for the `PSScriptAnalyzer` module correctly.
- Pester `RepoRoot` now resolves to the repository root, and the error-output
  regex no longer uses an invalid escape sequence.

### Repository cleanup

- Corrected the README feature count from "200+ Custom Functions" to
  "70+ Custom Functions", which is what the profile actually defines. The
  original figure overstated the project by roughly 3x.
- Renamed `python/task bar.py` to `python/task_bar.py`.
- Renamed `python/wifi detector.py` to `python/wifi_detector.py`.
- Renamed `python/taskmaneger.py` to `python/task_manager.py`, fixing a typo.
- Updated all README references to the new Python filenames. The README had
  documented `taskmanager.py`, a file that never existed.
- Normalized all text files to LF, ending a spurious 4,054-line diff in which
  every file appeared fully modified.
- Sorted imports, removed trailing whitespace, and added the missing final
  newline across the Python tools.
- Replaced the mutable default argument `languages=['en']` in
  `download_subtitles` with a `None` sentinel.

### Added (Python)

- `#!/usr/bin/env python3` shebang to every tool in `python/`, so the
  executable files can be run directly on POSIX systems.

## [Unreleased history]

Commits before this changelog was introduced have no recorded categorization.