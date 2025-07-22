# Python-SQLi-Lab 💉

A Flask web application designed for education and practice of SQL Injection vulnerabilities. This project provides various SQLi scenarios in a safe and controlled environment.

## 🎯 Purpose

Python-SQLi-Lab was created with the following purposes:

-   Education about different types of SQL Injection vulnerabilities
-   Providing a safe practice environment for security researchers
-   Helping developers understand how SQLi attacks work for better prevention
-   Supporting learning and research in web security

## 🛠️ Technologies Used

-   **Backend**: Flask (Python)
-   **Database**: MySQL 9.2
-   **Frontend**: HTML Templates with Jinja2
-   **Containerization**: Docker & Docker Compose
-   **Environment Management**: python-dotenv

## 📋 System Requirements

-   Docker and Docker Compose
-   Python 3.12+ (if running locally)
-   MySQL (if running locally)

## 🚀 Installation and Setup

### Using Docker (Recommended)

1. **Clone repository:**

```bash
git clone https://github.com/d4ngkh04w/Python-SQLi-Lab.git
cd Python-SQLi-Lab
```

2. **Create environment file (optional):**

```bash
# Create .env file
echo "DB_ROOT_PASSWORD=your_secure_password" > .env
echo "SECRET_KEY=your_secret_key" >> .env
```

3. **Start the application:**

```bash
docker compose up -d
```

4. **Access the application:**
    - Open your browser and visit: `http://localhost:1303`

### Local Development

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Configure database:**

    - Ensure MySQL is running
    - Create `sqli_lab` database
    - Update connection information in `.env` file

3. **Run the application:**

```bash
python app.py
```

## 🏆 Flags and Challenges

The application contains hidden flags that can be exploited through SQL Injection:

-   **FLAG_1**: Can be obtained through basic SQLi with admin role
-   **FLAG_2**: Stored in the database, requires exploitation to extract

## ⚠️ Security Warning

**IMPORTANT**: This application is intentionally designed with security vulnerabilities for educational purposes.

-   **DO NOT** use in production environments
-   **DO NOT** expose to the public internet
-   Only use in controlled learning and research environments

## 📝 License

This project is distributed under the MIT license. See the `LICENSE` file for more details.
