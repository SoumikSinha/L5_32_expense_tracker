# Lab 5: Reflection on Static Code Analysis

### 1. What was the most significant issue uncovered by the static analysis tools, and why?
The biggest issue was in `openStatement()` where `os.system("xdg-open " + path)` was used. Bandit flagged this as a command injection risk (B605). Because `os.system` runs commands through the system shell, passing any uncleaned path string could let an attacker inject extra shell commands (like using `;` or `&&`). Fixing it with `subprocess.run` using a list of arguments without `shell=True` avoids this issue. Also, having the hardcoded password `demo-sync-pass` right in the source code was another major security flaw flagged by Bandit (B105).

### 2. How do tools like Pylint, Bandit, and Flake8 complement each other during development?
Each of the three tools checks for different kinds of problems:
- **Bandit** checks for security vulnerabilities and unsafe functions (like hardcoded passwords, `tempfile.mktemp`, and unsafe shell commands).
- **Flake8** acts as a style and syntax checker, making sure the code follows standard PEP 8 formatting rules (like proper line lengths, blank lines, and whitespace around operators).
- **Pylint** does a deeper code quality check, catching things like overly broad exceptions (`except Exception`), missing docstrings, naming issues, and unused variables.
Using all three together helps catch security holes, messy style, and code smells at the same time.

### 3. How can integrating static code analysis into a CI/CD pipeline improve software reliability and security?
Adding these tools to automated CI/CD checks (like GitHub Actions) ensures that whenever someone pushes code or creates a pull request, the code is tested automatically before it gets merged. This catches insecure code, bugs, and bad formatting early so that developers do not have to waste time finding style mistakes manually during code reviews, and prevents broken or vulnerable code from reaching production.

### 4. What trade-offs exist between strict static analysis rules and development velocity?
If static analysis rules are too strict, they can slow down development because developers spend extra time fixing minor warnings that do not actually cause bugs (such as variable naming styles or strict line length limits). On the other hand, if rules are too loose, real bugs and security risks slip through. The best approach is to make security checks (like Bandit) mandatory, while using automatic formatters (like Black or autopep8) to handle style rules automatically without slowing down coding.
