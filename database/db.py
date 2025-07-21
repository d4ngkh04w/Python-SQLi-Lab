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
    admin_password = os.urandom(12).hex()
    user_password = "secret"

    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO users (username, password, role, secret) VALUES
            (%s, %s, 'admin', %s),
            (%s, %s, 'user', NULL)
        """,
        ("admin", admin_password, FLAG_1, "user", user_password),
    )

    cursor.execute(
        """
        INSERT INTO blogs (title, author_name) VALUES
            ('Lập trình Python cơ bản', 'Nguyễn Văn A'),
            ('Tìm hiểu về Docker', 'Trần Thị B'),
            ('Hướng dẫn sử dụng Git hiệu quả', 'Lê Văn C'),
            ('5 thư viện Python cho khoa học dữ liệu', 'Phạm Thị D'),
            ('Làm quen với ReactJS', 'Ngô Minh E'),
            ('Cách tối ưu hóa hiệu suất JavaScript', 'Đỗ Thị F'),
            ('Machine Learning cho người mới bắt đầu', 'Vũ Văn G'),
            ('REST API với Flask và Python', 'Hoàng Thị H'),
            ('CSS Grid vs Flexbox: Khi nào dùng gì?', 'Phan Văn I'),
            ('Bảo mật web: Những điều cơ bản cần biết', 'Trịnh Thị J'),
            ('Node.js và MongoDB: Xây dựng ứng dụng fullstack', 'Lý Văn K'),
            ('TypeScript: Tại sao bạn nên học?', 'Bùi Thị L'),
            ('DevOps cơ bản: CI/CD với GitHub Actions', 'Đặng Văn M'),
            ('Vue.js 3: Những tính năng mới đáng chú ý', 'Nguyễn Thị N'),
            ('SQL Injection và cách phòng chống', 'Tô Văn O'),
            ('Redis: Cache và Session Store hiệu quả', 'Đinh Thị P'),
            ('Design Patterns trong lập trình OOP', 'Mai Văn Q'),
            ('Microservices vs Monolith: Chọn kiến trúc nào?', 'Lại Thị R'),
            ('Kubernetes cơ bản cho Developer', 'Chu Văn S'),
            ('Clean Code: Viết code sạch và dễ maintain', 'Dương Thị T'),
            ('AWS Lambda: Serverless Computing thực tế', 'Phùng Văn U'),
            ('GraphQL vs REST: So sánh chi tiết', 'Ông Thị V'),
            ('Unit Testing với Jest và Python unittest', 'Hồ Văn W'),
            ('Blockchain và Smart Contract cơ bản', 'Võ Thị X'),
            ('Performance Testing với JMeter', 'Lưu Văn Y'),
            ('Mobile App Development với React Native', 'Cao Thị Z'),
            ('Data Science với Pandas và NumPy', 'Hà Văn AA'),
            ('Elasticsearch: Tìm kiếm và phân tích dữ liệu', 'Kiều Thị BB'),
            ('OAuth 2.0 và JWT trong Authentication', 'Lương Văn CC'),
            ('Agile và Scrum: Methodology cho team hiệu quả', 'Mạc Thị DD'),
            ('Progressive Web Apps (PWA): Tương lai của web', 'Ninh Văn EE'),
            ('Apache Kafka: Message Queue cho hệ thống lớn', 'Ô Thị FF'),
            ('Code Review: Best Practices và Tools', 'Quách Văn GG'),
            ('Cyber Security: Bảo vệ ứng dụng web', 'Sầm Thị HH'),
            ('Flutter vs React Native: Chọn framework nào?', 'Tạ Văn II'),
            ('Big Data với Apache Spark', 'Uyên Thị JJ'),
            ('Monitoring và Logging trong Production', 'Vương Văn KK'),
            ('API Design: RESTful best practices', 'Xa Thị LL'),
            ('Git Advanced: Rebase, Cherry-pick và Hooks', 'Yêu Văn MM'),
            ('Load Balancing và High Availability', 'Zung Thị NN');
        """
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
