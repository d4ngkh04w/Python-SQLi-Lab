# Python-SQLi-Lab 💉

A comprehensive educational platform for learning SQL injection vulnerabilities and prevention techniques. This lab provides hands-on experience with various types of SQL injection attacks in a safe, controlled environment.

## 🎯 Educational Objectives

- Understand different types of SQL injection vulnerabilities
- Learn how SQL injection attacks work in practice
- Compare vulnerable code with secure implementations
- Practice exploitation techniques ethically
- Learn prevention and mitigation strategies

## 🏗️ Project Structure

```
Python-SQLi-Lab/
├── app.py                  # Main Flask application (intentionally vulnerable)
├── database/
│   └── db.py              # Database setup and connection management
├── rce/
│   ├── exploit.py         # Advanced exploitation scripts
│   ├── raptor_udf2.c      # UDF source code for RCE
│   └── raptor_udf2.so     # Compiled UDF library
├── templates/             # HTML templates for web interface
├── static/               # Static web assets
├── secure_examples.py    # Secure coding examples (NEW)
├── CODE_REVIEW.md        # Comprehensive code review (NEW)
├── test_improvements.py  # Code quality tests (NEW)
└── README.md            # This file
```

## 🚨 Security Notice

**⚠️ WARNING**: This application contains intentional security vulnerabilities for educational purposes only.

- **DO NOT** deploy this in production environments
- **DO NOT** use this code as a template for real applications
- Only run in isolated, controlled environments (like Docker containers)
- Review `secure_examples.py` for proper security implementations

## 🔍 Vulnerability Types Demonstrated

### 1. Basic SQL Injection (`/sqli/basic`)
- **Type**: Authentication bypass
- **Method**: String concatenation in WHERE clause
- **Example**: `username: admin' OR '1'='1' --`
- **Learning Goal**: Understand fundamental SQLi concepts

### 2. UNION-based SQL Injection (`/sqli/union`)
- **Type**: Data extraction
- **Method**: UNION operator to combine queries
- **Example**: `search: test' UNION SELECT username,password FROM users--`
- **Learning Goal**: Learn advanced data extraction techniques

### 3. Error-based SQL Injection (`/sqli/error`)
- **Type**: Information disclosure
- **Method**: Triggering database errors to reveal information
- **Example**: `search: test' AND (SELECT * FROM information_schema.tables)--`
- **Learning Goal**: Understand error-based data extraction

### 4. Boolean-based Blind SQL Injection (`/sqli/boolean`)
- **Type**: Inference-based attacks
- **Method**: True/false responses to infer data
- **Example**: `search: admin' AND LENGTH(password)>10--`
- **Learning Goal**: Master blind injection techniques

### 5. Time-based Blind SQL Injection (`/sqli/time`)
- **Type**: Time-delay based inference
- **Method**: Using SLEEP() functions for data extraction
- **Example**: `search: admin' AND IF(LENGTH(password)>10,SLEEP(5),0)--`
- **Learning Goal**: Advanced blind injection with timing

### 6. SQL Injection to RCE (`/sqli/rce`)
- **Type**: Remote code execution
- **Method**: File operations and UDF functions
- **Example**: Advanced exploitation using `raptor_udf2.so`
- **Learning Goal**: Understand escalation from SQLi to RCE

## 🚀 Installation and Setup

### Option 1: Docker (Recommended)

1. **Clone the repository:**
```bash
git clone https://github.com/d4ngkh04w/Python-SQLi-Lab.git
cd Python-SQLi-Lab
```

2. **Build and start the container:**
```bash
docker build -t python-sqli-lab .
docker run -d -p 1303:1303 --name sqli-lab python-sqli-lab
```

3. **Access the application:**
   - Open your browser and navigate to: `http://localhost:1303`
   - The application will automatically initialize the database with sample data

### Option 2: Local Installation

1. **Prerequisites:**
   - Python 3.8+
   - MySQL Server
   - Required Python packages (see `requirements.txt`)

2. **Setup:**
```bash
# Install dependencies
pip install -r requirements.txt

# Configure MySQL (update connection details in database/db.py if needed)
# Default: host=127.0.0.1, user=root, password=root, database=sqli_lab

# Run the application
python3 app.py
```

## 📚 Learning Resources

### Code Review and Security Analysis
- Read `CODE_REVIEW.md` for comprehensive security analysis
- Review `secure_examples.py` for proper security implementations
- Compare vulnerable code in `app.py` with secure alternatives

### Hands-on Labs

1. **Basic Authentication Bypass:**
   - Navigate to `/sqli/basic`
   - Try logging in with: `admin' OR '1'='1' --`
   - Observe the authentication bypass

2. **Data Extraction with UNION:**
   - Go to `/sqli/union`
   - Search for: `test' UNION SELECT username,password FROM users--`
   - Extract user credentials

3. **Advanced RCE Exploitation:**
   - Use the exploit script: `python3 rce/exploit.py --help`
   - Follow the RCE demonstration carefully

### Testing Your Understanding
```bash
# Run the test suite to verify your environment
python3 test_improvements.py

# Demonstrate secure coding practices
python3 secure_examples.py
```

## 🛡️ Security Best Practices (Prevention)

The `secure_examples.py` module demonstrates proper security implementations:

### 1. Use Parameterized Queries
```python
# ❌ Vulnerable
cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")

# ✅ Secure
cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
```

### 2. Input Validation
```python
# ✅ Secure approach
def validate_username(username):
    if not username or len(username) > 20:
        return False
    return username.replace('_', '').isalnum()
```

### 3. Proper Error Handling
```python
# ❌ Vulnerable - exposes database errors
except mysql.connector.Error as e:
    return f"Database error: {str(e)}"

# ✅ Secure - logs details, returns generic error
except mysql.connector.Error as e:
    logger.error(f"Database error: {e}")
    return "An error occurred"
```

## 🧪 Advanced Exploitation

### Using the Automated Exploit
```bash
# Basic exploitation setup
python3 rce/exploit.py

# Execute custom commands via RCE
python3 rce/exploit.py --rce "id"

# Help and usage
python3 rce/exploit.py --help
```

### Manual Exploitation Steps
1. **Identify injection point**: Find vulnerable parameter
2. **Determine database type**: Test MySQL-specific functions
3. **Extract schema information**: Use information_schema tables
4. **Escalate to file operations**: Test file read/write permissions
5. **Achieve RCE**: Upload UDF libraries for code execution

## 🔧 Development and Contribution

### Code Quality Standards
- All code includes educational comments explaining vulnerabilities
- Secure alternatives are provided in `secure_examples.py`
- Regular testing with `test_improvements.py`
- Documentation updates reflect code changes

### Running Tests
```bash
# Run all quality tests
python3 test_improvements.py

# Compile-check all Python files
python3 -m py_compile app.py database/db.py secure_examples.py
```

## 📖 Educational Notes

### For Instructors
- Use this lab to demonstrate real-world attack scenarios
- Compare vulnerable and secure code side-by-side
- Emphasize the importance of secure coding practices
- Discuss the impact of SQL injection on real applications

### For Students
- Start with basic injection before moving to advanced techniques
- Practice on each vulnerability type systematically
- Read the code to understand why vulnerabilities exist
- Study the secure examples to learn prevention methods

## 🆘 Troubleshooting

### Common Issues
1. **Database connection failed**: Check MySQL service and credentials
2. **Permission denied**: Ensure proper file permissions for UDF operations
3. **Module not found**: Install dependencies with `pip install -r requirements.txt`

### Getting Help
- Review the comprehensive `CODE_REVIEW.md`
- Check logs for detailed error information
- Ensure Docker/MySQL is properly configured

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚖️ Ethical Use Statement

This educational tool is provided for legitimate security education and authorized penetration testing only. Users are responsible for ensuring their use complies with applicable laws and regulations. The authors do not condone or support malicious use of these techniques.

---

**Remember**: The goal is to learn how to build secure applications by understanding how attacks work! 🛡️
