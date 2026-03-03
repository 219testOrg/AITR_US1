# Vulnerable Python Application

This project is specifically designed for testing remediation agents. It contains **intentional security vulnerabilities** and should **never** be deployed in a production environment.

## Purpose

The purpose of this application is to:
- Test security scanning tools
- Evaluate remediation agents
- Demonstrate common vulnerabilities in Python applications
- Serve as an educational resource for security testing

## Vulnerabilities

This application contains many intentional security vulnerabilities, including but not limited to:

1. Outdated dependencies with known CVEs
2. SQL injection vulnerabilities
3. Command injection vulnerabilities
4. Insecure deserialization
5. Hardcoded credentials
6. Weak cryptography
7. Path traversal
8. Server-side template injection
9. Insecure direct object references
10. XML external entity vulnerabilities
11. JWT vulnerabilities

## Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```
   python database.py
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Run the API server (in a separate terminal):
   ```
   python api.py
   ```

## Warning

This application is intentionally vulnerable and should only be used for testing purposes in a controlled environment. DO NOT use this code in any production environment or expose it to the internet.

## License

This project is for educational purposes only. 