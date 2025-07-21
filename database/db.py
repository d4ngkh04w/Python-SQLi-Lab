import os, time
import mysql.connector, mysql.connector.abstracts
import dotenv

dotenv.load_dotenv()

FLAG_1 = f"FLAG{{{os.urandom(12).hex()}}}"
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
            username VARCHAR(20) NOT NULL UNIQUE,
            password VARCHAR(50) NOT NULL,
            role VARCHAR(20) DEFAULT 'user',
            secret TEXT,
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
        ("admin", f"{os.urandom(12).hex()}", "admin", FLAG_1),
        ("alice", f"{os.urandom(12).hex()}", "user", None),
        ("bob", f"{os.urandom(12).hex()}", "user", None),
        ("charlie", f"{os.urandom(12).hex()}", "user", None),
        ("diana", f"{os.urandom(12).hex()}", "user", None),
        ("edward", f"{os.urandom(12).hex()}", "user", None),
        ("fiona", f"{os.urandom(12).hex()}", "user", None),
        ("george", f"{os.urandom(12).hex()}", "user", None),
        ("helen", f"{os.urandom(12).hex()}", "user", None),
        ("ivan", f"{os.urandom(12).hex()}", "user", None),
        ("julia", f"{os.urandom(12).hex()}", "user", None),
        ("kevin", f"{os.urandom(12).hex()}", "user", None),
        ("linda", f"{os.urandom(12).hex()}", "user", None),
        ("martin", f"{os.urandom(12).hex()}", "user", None),
        ("nancy", f"{os.urandom(12).hex()}", "user", None),
        ("oscar", f"{os.urandom(12).hex()}", "user", None),
        ("penny", f"{os.urandom(12).hex()}", "user", None),
        ("quincy", f"{os.urandom(12).hex()}", "user", None),
        ("rachel", f"{os.urandom(12).hex()}", "user", None),
        ("steve", f"{os.urandom(12).hex()}", "user", None),
        ("tina", f"{os.urandom(12).hex()}", "user", None),
        ("victor", f"{os.urandom(12).hex()}", "user", None),
        ("wendy", f"{os.urandom(12).hex()}", "user", None),
        ("xavier", f"{os.urandom(12).hex()}", "user", None),
        ("yvonne", f"{os.urandom(12).hex()}", "user", None),
        ("zack", f"{os.urandom(12).hex()}", "user", None),
    ]

    for username, password, role, secret in users_data:
        cursor.execute(
            """
            INSERT INTO users (username, password, role, secret) VALUES
                (%s, %s, %s, %s);
            """,
            (username, password, role, secret),
        )

    # Insert blogs with author_name matching usernames
    blogs_data = [
        ("Lập trình Python cơ bản", "alice"),
        ("Tìm hiểu về Docker", "bob"),
        ("Hướng dẫn sử dụng Git hiệu quả", "charlie"),
        ("5 thư viện Python cho khoa học dữ liệu", "diana"),
        ("Làm quen với ReactJS", "edward"),
        ("Cách tối ưu hóa hiệu suất JavaScript", "fiona"),
        ("Machine Learning cho người mới bắt đầu", "george"),
        ("REST API với Flask và Python", "helen"),
        ("CSS Grid vs Flexbox: Khi nào dùng gì?", "ivan"),
        ("Bảo mật web: Những điều cơ bản cần biết", "julia"),
        ("Node.js và MongoDB: Xây dựng ứng dụng fullstack", "kevin"),
        ("TypeScript: Tại sao bạn nên học?", "linda"),
        ("DevOps cơ bản: CI/CD với GitHub Actions", "martin"),
        ("Vue.js 3: Những tính năng mới đáng chú ý", "nancy"),
        ("SQL Injection và cách phòng chống", "oscar"),
        ("Redis: Cache và Session Store hiệu quả", "penny"),
        ("Design Patterns trong lập trình OOP", "quincy"),
        ("Microservices vs Monolith: Chọn kiến trúc nào?", "rachel"),
        ("Kubernetes cơ bản cho Developer", "steve"),
        ("Clean Code: Viết code sạch và dễ maintain", "tina"),
        ("AWS Lambda: Serverless Computing thực tế", "victor"),
        ("GraphQL vs REST: So sánh chi tiết", "wendy"),
        ("Unit Testing với Jest và Python unittest", "xavier"),
        ("Blockchain và Smart Contract cơ bản", "yvonne"),
        ("Performance Testing với JMeter", "zack"),
        ("Mobile App Development với React Native", "alice"),
        ("Data Science với Pandas và NumPy", "bob"),
        ("Elasticsearch: Tìm kiếm và phân tích dữ liệu", "charlie"),
        ("OAuth 2.0 và JWT trong Authentication", "diana"),
        ("Agile và Scrum: Methodology cho team hiệu quả", "edward"),
        ("Progressive Web Apps (PWA): Tương lai của web", "fiona"),
        ("Apache Kafka: Message Queue cho hệ thống lớn", "george"),
        ("Code Review: Best Practices và Tools", "helen"),
        ("Cyber Security: Bảo vệ ứng dụng web", "ivan"),
        ("Flutter vs React Native: Chọn framework nào?", "julia"),
        ("Big Data với Apache Spark", "kevin"),
        ("Monitoring và Logging trong Production", "linda"),
        ("API Design: RESTful best practices", "martin"),
        ("Git Advanced: Rebase, Cherry-pick và Hooks", "nancy"),
        ("Load Balancing và High Availability", "oscar"),
        ("Containerization với Docker và Kubernetes", "penny"),
        ("Microservices Architecture Best Practices", "quincy"),
        ("Web Security và Penetration Testing", "rachel"),
        ("Cloud Computing với AWS và Azure", "steve"),
        ("Database Optimization và Performance Tuning", "tina"),
        ("Frontend Frameworks: React vs Vue vs Angular", "victor"),
        ("Backend Development với Node.js và Express", "wendy"),
        ("Data Analysis với Python và R", "xavier"),
        ("Mobile Development: Native vs Cross-platform", "yvonne"),
        ("DevSecOps: Security trong CI/CD Pipeline", "zack"),
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
