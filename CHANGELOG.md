# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

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