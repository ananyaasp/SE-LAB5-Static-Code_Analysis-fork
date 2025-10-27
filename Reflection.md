Reflection
1. Which issues were the easiest to fix, and which were the hardest? Why?
•	Easiest fixes:
Formatting issues such as line length (E501) and whitespace (W293) were the simplest because they only required splitting long lines or removing extra spaces without affecting logic.
Adding docstrings was also easy since it only involved describing the purpose and parameters of existing functions and didn’t require code modifications.
•	Hardest fixes:
The most challenging part was replacing the broad except: statements with specific exception types like OSError, KeyError, and JSONDecodeError.
I had to carefully trace which errors might actually occur in each block (e.g., when loading JSON from file vs. accessing inventory keys).
Implementing input validation for quantity (qty <= 0) was also tricky because I had to ensure it didn’t break existing logic that depended on these values.

3. Did the static analysis tools report any false positives? If so, describe one example.
•	Yes. Bandit flagged the use of file I/O (open() function) as a potential security risk, even though my use case was strictly for local inventory data and not user-uploaded files.
This warning was technically correct from a security perspective, but in the context of this controlled environment, it did not pose an actual risk.
Therefore, I classified it as a false positive.

4. How would you integrate static analysis tools into your actual development workflow?
•	I would set up pre-commit hooks so that Flake8 and Pylint automatically scan the code before it is committed. This would catch formatting and documentation issues early.
•	For continuous improvement, I would integrate Bandit into a CI pipeline using GitHub Actions so that any insecure coding practices are flagged during pull requests.
•	This approach ensures that issues like broad exception handling and missing documentation are proactively prevented rather than fixed after development.

5. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?
•	The code is now more reliable due to specific exception handling, which prevents unexpected crashes and makes debugging easier.
•	Data validation improvements ensure the system cannot mistakenly add negative or zero quantities, which directly improves the robustness of inventory calculations.
•	Using consistent f-strings improved readability and made the logging output more standardized.
•	Removing hardcoded file names made the system more reusable, allowing external file paths to be passed dynamically.
•	Overall, static analysis helped reduce silent failures and made the codebase more maintainable and production-ready.
