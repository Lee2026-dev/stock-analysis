## [2026-02-04] Dependency Issues
- **pandas-ta**: Installation failed because it allegedly requires Python >= 3.12, but our environment is 3.9.6. 
- **Workaround**: Removed `pandas-ta` from `pyproject.toml`. We may need to find a compatible version or implement technical indicators manually in Phase 2.
