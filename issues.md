# Lab 5: Identified and Resolved Issues

## Issue Summary Table

| Issue | Tool / Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| B105: Hardcoded Password | Bandit (Security) | 5 | Hardcoded password string `demo-sync-pass` was assigned directly to `BANK_SYNC_PASSWORD`. | Read from environment variable `os.getenv("BANK_SYNC_PASS", "demo-sync-pass")`. |
| B306: Insecure Temp File | Bandit (Security) | 57 | Used deprecated `tempfile.mktemp()` which is vulnerable to race conditions. | Switched to `tempfile.NamedTemporaryFile` with explicit directory handling. |
| B605: Shell Command Injection | Bandit (Security) | 62 | `os.system("xdg-open " + path)` passes raw string to shell, risking command injection. | Replaced with `subprocess.run(["xdg-open", safe_path], check=False)` without shell. |
| B108: Hardcoded Insecure Path | Bandit (Security) | 8 | Direct usage of hardcoded `/tmp/expense_reports` path. | Used cross-platform temp directory with `os.path.join(tempfile.gettempdir(), "expense_reports")`. |
| W0703: Overly Broad Exception | Pylint (Warning) | 41 | Caught broad `Exception` in `biggestExpense()`. | Replaced with specific `ValueError` that `max()` raises on empty lists. |
| C0103: Non-PEP 8 Naming | Pylint / Flake8 | 11, 20, 28, 33, 38, 44, 49, 54, 60 | Function names used camelCase (e.g. `addExpense`). | Renamed functions to snake_case (`add_expense`, etc.) and kept aliases for compatibility. |
| E203, E302, E261, E501: Formatting | Flake8 (Style) | 15, 44, 74, 77 | Whitespace before colon, missing blank lines, lines longer than 79 chars. | Fixed dictionary spacing, added standard 2 blank lines before functions, wrapped long lines. |

## Verification
- Pylint score: improved from 5.27/10 to 10.00/10.
- Bandit findings: 0 issues.
- Flake8 warnings: 0 warnings.
- Output: Program output remains identical to the original demo.
