"""
Database Module for Python SQLi Lab

This module handles database connections and initialization for the educational
SQL injection demonstration application.

Educational Purpose: Shows database setup with intentionally insecure configurations
for learning about SQL injection vulnerabilities.
"""

import os, time
import mysql.connector, mysql.connector.abstracts
import logging

logger = logging.getLogger(__name__)

# Educational flag for advanced exploitation scenarios
FLAG_2 = f"FLAG{{{os.urandom(12).hex()}}}"


def get_db_connection():
    """
    Establish connection to MySQL database with retry logic.
    
    Educational note: Using hardcoded credentials for simplicity in lab environment.
    In production, use environment variables and secure credential management.
    
    Returns:
        mysql.connector connection object
    
    Raises:
        mysql.connector.Error: If connection fails after retries
    """
    for attempt in range(10):
        try:
            conn = mysql.connector.connect(
                host="127.0.0.1",
                port=3306,
                database="sqli_lab",
                user="root",
                password="root",  # Hardcoded for educational purposes
            )
            logger.info("Database connection established successfully")
            return conn
        except mysql.connector.Error as e:
            logger.warning(f"Connection attempt {attempt + 1} failed: {str(e)}. Retrying...")
            time.sleep(1.5)
    
    logger.error("Failed to connect to database after 10 attempts")
    raise mysql.connector.Error("Failed to connect to the database")


def create_tables(
    conn: (
        mysql.connector.pooling.PooledMySQLConnection
        | mysql.connector.abstracts.MySQLConnectionAbstract
    ),
):
    """
    Create database tables for the SQLi lab.
    
    Creates three tables:
    1. users - For authentication bypass demonstrations
    2. blogs - For UNION and error-based SQLi demonstrations  
    3. flag - For advanced exploitation scenarios
    
    Educational note: The table structure is designed to facilitate
    various SQL injection attack demonstrations.
    
    Args:
        conn: MySQL database connection
    """
    cursor = conn.cursor()
    logger.info("Dropping existing tables and creating fresh schema...")
    
    # Drop existing tables for clean setup
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS blogs")
    cursor.execute("DROP TABLE IF EXISTS flag")
    
    # Users table - for authentication bypass scenarios
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
            username VARCHAR(20) NOT NULL UNIQUE,
            password VARCHAR(50) NOT NULL,
            role VARCHAR(20) DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    logger.info("Created users table")

    # Blogs table - for UNION and search-based SQLi scenarios
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS blogs (
            id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(200) NOT NULL,
            author_name VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    logger.info("Created blogs table")

    # Flag table - for advanced exploitation scenarios
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS flag (
            flag TEXT NOT NULL
        );
        """
    )
    logger.info("Created flag table")


def init_data(
    conn: (
        mysql.connector.pooling.PooledMySQLConnection
        | mysql.connector.abstracts.MySQLConnectionAbstract
    ),
):
    """
    Initialize database with sample data for SQLi demonstrations.
    
    Populates tables with:
    - 26 users including one admin account for privilege escalation demos
    - 50 blog posts for search-based SQLi scenarios
    - Educational flags for capture-the-flag style learning
    
    Educational note: Passwords are randomly generated hex values.
    In real applications, passwords should be properly hashed.
    
    Args:
        conn: MySQL database connection
    """
    cursor = conn.cursor()
    logger.info("Initializing database with sample data...")

    # Educational user data with mixed privileges
    users_data = [
        ("alice", f"{os.urandom(12).hex()}", "user"),
        ("bob", f"{os.urandom(12).hex()}", "user"),
        ("charlie", f"{os.urandom(12).hex()}", "user"),
        ("diana", f"{os.urandom(12).hex()}", "user"),
        ("edward", f"{os.urandom(12).hex()}", "user"),
        ("fiona", f"{os.urandom(12).hex()}", "user"),
        ("george", f"{os.urandom(12).hex()}", "user"),
        ("helen", f"{os.urandom(12).hex()}", "user"),
        ("ivan", f"{os.urandom(12).hex()}", "user"),
        ("julia", f"{os.urandom(12).hex()}", "user"),
        ("kevin", f"{os.urandom(12).hex()}", "user"),
        ("admin", f"{os.urandom(12).hex()}", "admin"),  # Target for privilege escalation
        ("linda", f"{os.urandom(12).hex()}", "user"),
        ("martin", f"{os.urandom(12).hex()}", "user"),
        ("nancy", f"{os.urandom(12).hex()}", "user"),
        ("oscar", f"{os.urandom(12).hex()}", "user"),
        ("penny", f"{os.urandom(12).hex()}", "user"),
        ("quincy", f"{os.urandom(12).hex()}", "user"),
        ("rachel", f"{os.urandom(12).hex()}", "user"),
        ("steve", f"{os.urandom(12).hex()}", "user"),
        ("tina", f"{os.urandom(12).hex()}", "user"),
        ("victor", f"{os.urandom(12).hex()}", "user"),
        ("wendy", f"{os.urandom(12).hex()}", "user"),
        ("xavier", f"{os.urandom(12).hex()}", "user"),
        ("yvonne", f"{os.urandom(12).hex()}", "user"),
        ("zack", f"{os.urandom(12).hex()}", "user"),
    ]

    # Insert users with parameterized queries (showing secure practice in data setup)
    for username, password, role in users_data:
        cursor.execute(
            """
            INSERT INTO users (username, password, role) VALUES
                (%s, %s, %s);
            """,
            (username, password, role),
        )
    
    logger.info(f"Inserted {len(users_data)} users (including 1 admin)")

    # Educational blog data for search-based SQLi demonstrations
    blogs_data = [
        ("Basic Python Programming", "alice"),
        ("Introduction to Docker", "bob"),
        ("Effective Git Usage Guide", "charlie"),
        ("5 Python Libraries for Data Science", "diana"),
        ("Getting Started with ReactJS", "edward"),
        ("How to Optimize JavaScript Performance", "fiona"),
        ("Machine Learning for Beginners", "george"),
        ("REST API with Flask and Python", "helen"),
        ("CSS Grid vs Flexbox: When to Use What?", "ivan"),
        ("Web Security: Basic Things You Need to Know", "julia"),
        ("Node.js and MongoDB: Building Fullstack Applications", "kevin"),
        ("TypeScript: Why Should You Learn It?", "linda"),
        ("Basic DevOps: CI/CD with GitHub Actions", "martin"),
        ("Vue.js 3: Notable New Features", "nancy"),
        ("SQL Injection and Prevention Methods", "oscar"),
        ("Redis: Efficient Cache and Session Store", "penny"),
        ("Design Patterns in OOP Programming", "quincy"),
        ("Microservices vs Monolith: Which Architecture to Choose?", "rachel"),
        ("Kubernetes Basics for Developers", "steve"),
        ("Clean Code: Writing Clean and Maintainable Code", "tina"),
        ("AWS Lambda: Practical Serverless Computing", "victor"),
        ("GraphQL vs REST: Detailed Comparison", "wendy"),
        ("Unit Testing with Jest and Python unittest", "xavier"),
        ("Blockchain and Smart Contract Basics", "yvonne"),
        ("Performance Testing with JMeter", "zack"),
        ("Mobile App Development with React Native", "alice"),
        ("Data Science with Pandas and NumPy", "bob"),
        ("Elasticsearch: Data Search and Analysis", "charlie"),
        ("OAuth 2.0 and JWT in Authentication", "diana"),
        ("Agile and Scrum: Methodology for Effective Teams", "edward"),
        ("Progressive Web Apps (PWA): The Future of Web", "fiona"),
        ("Apache Kafka: Message Queue for Large Systems", "george"),
        ("Code Review: Best Practices and Tools", "helen"),
        ("Cyber Security: Protecting Web Applications", "ivan"),
        ("Flutter vs React Native: Which Framework to Choose?", "julia"),
        ("Big Data with Apache Spark", "kevin"),
        ("Monitoring and Logging in Production", "linda"),
        ("API Design: RESTful Best Practices", "martin"),
        ("Git Advanced: Rebase, Cherry-pick and Hooks", "nancy"),
        ("Load Balancing and High Availability", "oscar"),
        ("Containerization with Docker and Kubernetes", "penny"),
        ("Microservices Architecture Best Practices", "quincy"),
        ("Web Security and Penetration Testing", "rachel"),
        ("Cloud Computing with AWS and Azure", "steve"),
        ("Database Optimization and Performance Tuning", "tina"),
        ("Frontend Frameworks: React vs Vue vs Angular", "victor"),
        ("Backend Development with Node.js and Express", "wendy"),
        ("Data Analysis with Python and R", "xavier"),
        ("Mobile Development: Native vs Cross-platform", "yvonne"),
        ("DevSecOps: Security in CI/CD Pipeline", "zack"),
    ]

    # Insert blog data using parameterized queries
    for title, author_name in blogs_data:
        cursor.execute(
            """
            INSERT INTO blogs (title, author_name) VALUES (%s, %s);
            """,
            (title, author_name),
        )
    
    logger.info(f"Inserted {len(blogs_data)} blog posts")

    # Insert educational flag for advanced scenarios
    cursor.execute(
        """
        INSERT INTO flag (flag) VALUES
            (%s);
        """,
        (FLAG_2,),
    )
    logger.info("Inserted educational flag")


def main():
    """
    Main initialization function for the SQLi lab database.
    
    Sets up the complete database environment with tables and sample data.
    This function should be called once during application startup.
    
    Educational note: This creates a completely fresh database each time,
    which is suitable for a lab environment but not for production use.
    """
    logger.info("Starting database initialization...")
    
    try:
        conn = get_db_connection()
        create_tables(conn)
        init_data(conn)
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully!")
        print("Database initialized successfully!")
    except mysql.connector.Error as e:
        logger.error(f"Database initialization failed: {e}")
        print(f"Database initialization failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during database initialization: {e}")
        print(f"Unexpected error during database initialization: {e}")
        raise
