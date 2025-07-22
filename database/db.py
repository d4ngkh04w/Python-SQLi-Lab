import os, time
import mysql.connector, mysql.connector.abstracts
import dotenv

dotenv.load_dotenv()

FLAG_2 = f"FLAG{{{os.urandom(12).hex()}}}"

HOST = os.getenv("DB_HOST", "127.0.0.1")
PASSWORD = os.getenv("DB_ROOT_PASSWORD")
PORT = int(os.getenv("DB_PORT", 3306))


def get_db_connection():
    for _ in range(10):
        try:
            conn = mysql.connector.connect(
                host=HOST,
                port=PORT,
                database="sqli_lab",
                user="root",
                password=PASSWORD,
            )
            return conn
        except mysql.connector.Error as e:
            print(f"Connection failed: {str(e)}. Retrying...")
            time.sleep(1.5)
    raise mysql.connector.Error("Failed to connect to the database")


def create_tables(
    conn: (
        mysql.connector.pooling.PooledMySQLConnection
        | mysql.connector.abstracts.MySQLConnectionAbstract
    ),
):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS blogs")
    cursor.execute("DROP TABLE IF EXISTS flag")
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

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS flag (
            flag TEXT NOT NULL
        );
        """
    )


def init_data(
    conn: (
        mysql.connector.pooling.PooledMySQLConnection
        | mysql.connector.abstracts.MySQLConnectionAbstract
    ),
):

    cursor = conn.cursor()

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
        ("admin", f"{os.urandom(12).hex()}", "admin"),
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

    for username, password, role in users_data:
        cursor.execute(
            """
            INSERT INTO users (username, password, role) VALUES
                (%s, %s, %s);
            """,
            (username, password, role),
        )

    # Insert blogs with author_name matching usernames
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

    for title, author_name in blogs_data:
        cursor.execute(
            """
            INSERT INTO blogs (title, author_name) VALUES (%s, %s);
            """,
            (title, author_name),
        )

    cursor.execute(
        """
        INSERT INTO flag (flag) VALUES
            (%s);
        """,
        (FLAG_2,),
    )


def main():
    conn = get_db_connection()
    create_tables(conn)
    init_data(conn)
    conn.commit()
    conn.close()
    print("Database initialized successfully!")
