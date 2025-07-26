"""
Python SQLi Lab - Educational SQL Injection Demonstration

This application intentionally contains SQL injection vulnerabilities for educational purposes.
DO NOT use this code in production environments.

Author: Educational Security Demonstration
Purpose: Teaching SQL injection attack vectors and prevention methods
"""

import flask
import os, time
import database.db as db
import mysql.connector
from datetime import timedelta
import logging

# Configure logging for educational purposes
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = flask.Flask(__name__)
app.secret_key = os.urandom(24).hex()

app.permanent_session_lifetime = timedelta(minutes=5)

# Educational flag for demonstration purposes
FLAG_1 = f"FLAG{{{os.urandom(12).hex()}}}"


@app.route("/", methods=["GET", "POST"])
def home():
    return flask.render_template("home.html")


@app.route("/sqli/basic/profile", methods=["GET"])
def profile():
    username = flask.session.get("username", "Guest")
    secret = flask.session.get("secret")
    return flask.render_template("profile.html", username=username, secret=secret)


@app.route("/sqli/basic", methods=["GET", "POST"])
def sqli_basic():
    """
    VULNERABLE ENDPOINT - Basic SQL Injection Demonstration
    
    This endpoint demonstrates basic SQL injection vulnerabilities through
    string concatenation in SQL queries.
    
    Vulnerability: Direct string concatenation allows SQL injection
    Attack example: username = "admin' OR '1'='1' --"
    
    Educational note: In secure applications, use parameterized queries:
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    """
    error = None
    if flask.request.method == "POST":
        username = flask.request.form.get("username")
        password = flask.request.form.get("password")

        if username and password:
            # Log the attempt for educational analysis
            logger.info(f"Login attempt for username: {username}")

            conn = db.get_db_connection()
            cursor = conn.cursor(dictionary=True)

            try:
                # VULNERABLE CODE - String concatenation allows SQL injection
                query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
                logger.info(f"Executing query: {query}")  # Educational logging
                cursor.execute(query)

                user = cursor.fetchall()
                if user:
                    user = user[0]
                else:
                    user = None

                logger.info(f"Query result: {user}")
                if user:
                    flask.session["username"] = user.get("username")
                    if user.get("role") == "admin":
                        flask.session["secret"] = FLAG_1
                    else:
                        flask.session["secret"] = None
                    return flask.redirect("/sqli/basic/profile")
                else:
                    error = "Invalid credentials"
            except mysql.connector.Error as e:
                logger.error(f"Database error in basic SQLi: {e}")
                error = f"Internal Server Error"
            except Exception as e:
                logger.error(f"Unexpected error in basic SQLi: {e}")
                error = f"Internal Server Error"
            finally:
                cursor.close()
                conn.close()

    return flask.render_template("login.html", error=error)


@app.route("/sqli/union", methods=["GET"])
def sqli_union():
    """
    VULNERABLE ENDPOINT - UNION-based SQL Injection Demonstration
    
    This endpoint demonstrates UNION-based SQL injection vulnerabilities.
    
    Vulnerability: Direct string concatenation in LIKE clause
    Attack example: search = "test' UNION SELECT username,password FROM users--"
    
    Educational note: The UNION attack allows attackers to retrieve data from other tables
    by combining results from multiple SELECT statements.
    """
    blogs = []
    error = None

    search = flask.request.args.get("search", "")
    logger.info(f"Blog search request: {search}")

    if search:
        conn = db.get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # VULNERABLE CODE - String concatenation allows UNION injection
            query = f"SELECT title, author_name FROM blogs WHERE title LIKE '%{search}%'"
            logger.info(f"Executing query: {query}")  # Educational logging
            cursor.execute(query)

            blogs = cursor.fetchall()
            logger.info(f"Query returned {len(blogs)} results")
        except mysql.connector.Error as e:
            logger.error(f"Database error in UNION SQLi: {e}")
            error = f"Internal Server Error"
        except Exception as e:
            logger.error(f"Unexpected error in UNION SQLi: {e}")
            error = f"Internal Server Error"
        finally:
            cursor.close()
            conn.close()

    return flask.render_template("blog.html", blogs=blogs, error=error, search=search)


@app.route("/sqli/error", methods=["GET"])
def sqli_error():
    """
    VULNERABLE ENDPOINT - Error-based SQL Injection Demonstration
    
    This endpoint demonstrates error-based SQL injection where database errors
    are exposed to the user, potentially revealing sensitive information.
    
    Vulnerability: Error messages expose database structure and sensitive data
    Attack example: search = "test' AND (SELECT COUNT(*) FROM information_schema.tables)>0--"
    
    Educational note: Error-based attacks use database error messages to extract information.
    Secure applications should never expose detailed database errors to users.
    """
    blogs = []
    error = None

    search = flask.request.args.get("search", "")
    logger.info(f"Error-based SQLi search request: {search}")

    if search:
        conn = db.get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # VULNERABLE CODE - String concatenation allows error-based injection
            query = f"SELECT title, author_name FROM blogs WHERE title LIKE '%{search}%'"
            logger.info(f"Executing query: {query}")  # Educational logging
            cursor.execute(query)

            blogs = cursor.fetchall()
        except mysql.connector.Error as e:
            # VULNERABLE - Exposing detailed database errors to users
            logger.error(f"Database error (exposed to user): {e}")
            error = f"Database error: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error (exposed to user): {e}")
            error = f"An unexpected error occurred: {str(e)}"
        finally:
            cursor.close()
            conn.close()

    return flask.render_template("blog.html", blogs=blogs, error=error, search=search)


@app.route("/sqli/boolean", methods=["GET"])
def sqli_boolean():
    """
    VULNERABLE ENDPOINT - Boolean-based Blind SQL Injection Demonstration
    
    This endpoint demonstrates boolean-based blind SQL injection where
    attackers infer information based on application behavior (true/false responses).
    
    Vulnerability: Application behavior reveals query success/failure
    Attack example: search = "admin' AND (SELECT LENGTH(password) FROM users WHERE username='admin')>10--"
    
    Educational note: Boolean-based attacks use conditional logic to extract data
    bit by bit based on application responses.
    """
    search = flask.request.args.get("search", "")
    res = "Not found"
    logger.info(f"Boolean-based SQLi search request: {search}")

    if search != "":
        conn = db.get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # VULNERABLE CODE - String concatenation allows boolean-based injection
            query = f"SELECT * FROM users WHERE username = '{search}'"
            logger.info(f"Executing query: {query}")  # Educational logging
            cursor.execute(query)
            
            user = cursor.fetchall()
            if user:
                res = "Found"
                logger.info(f"Boolean result: {res} (user found)")
            else:
                logger.info(f"Boolean result: {res} (user not found)")

            return flask.render_template(
                "user.html", search=search, result=res, show_result=True
            )
        except mysql.connector.Error as e:
            logger.error(f"Database error in boolean SQLi: {e}")
            return flask.render_template(
                "user.html", search=search, result=res, show_result=True
            )
        except Exception as e:
            logger.error(f"Unexpected error in boolean SQLi: {e}")
            return flask.render_template(
                "user.html", search=search, result=res, show_result=True
            )
        finally:
            cursor.close()
            conn.close()

    return flask.render_template("user.html", search=search, show_result=True)


@app.route("/sqli/time", methods=["GET"])
def sqli_time():
    """
    VULNERABLE ENDPOINT - Time-based Blind SQL Injection Demonstration
    
    This endpoint demonstrates time-based blind SQL injection where
    attackers infer information based on response timing.
    
    Vulnerability: Time delays can be used to extract information
    Attack example: search = "admin' AND IF((SELECT LENGTH(password) FROM users WHERE username='admin')>10,SLEEP(5),0)--"
    
    Educational note: Time-based attacks use conditional delays to extract data
    when no other feedback mechanism is available.
    """
    search = flask.request.args.get("search", "")
    logger.info(f"Time-based SQLi search request: {search}")

    if search != "":
        conn = db.get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # Measure execution time for educational purposes
            start = time.time()
            
            # VULNERABLE CODE - String concatenation allows time-based injection
            query = f"SELECT * FROM users WHERE username = '{search}'"
            logger.info(f"Executing query: {query}")  # Educational logging
            cursor.execute(query)
            
            end = time.time()
            execution_time = end - start
            logger.info(f"Query execution time: {execution_time:.4f} seconds")

            if cursor.fetchall():
                return flask.render_template("user.html", search=search, result="Found")
        except mysql.connector.Error as e:
            logger.error(f"Database error in time-based SQLi: {e}")
            return flask.render_template("user.html", search=search, result="Not found")
        except Exception as e:
            logger.error(f"Unexpected error in time-based SQLi: {e}")
            return flask.render_template("user.html", search=search, result="Not found")
        finally:
            cursor.close()
            conn.close()

    return flask.render_template("user.html", search=search)


@app.route("/sqli/rce", methods=["GET"])
def sqli_to_rce():
    """
    VULNERABLE ENDPOINT - SQL Injection to Remote Code Execution
    
    This endpoint demonstrates how SQL injection can be escalated to
    Remote Code Execution (RCE) through file operations and UDF functions.
    
    Vulnerability: SQLi combined with file operations enables RCE
    Educational note: This shows advanced exploitation techniques where
    SQL injection can lead to complete system compromise.
    """
    blogs = []
    error = None

    search = flask.request.args.get("search", "")
    logger.info(f"SQLi to RCE search request: {search}")

    if search:
        conn = db.get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # VULNERABLE CODE - String concatenation allows advanced SQLi for RCE
            query = f"SELECT title, author_name FROM blogs WHERE title LIKE '%{search}%'"
            logger.info(f"Executing query: {query}")  # Educational logging
            cursor.execute(query)

            blogs = cursor.fetchall()
        except mysql.connector.Error as e:
            logger.error(f"Database error in RCE SQLi: {e}")
            print(f"Database error: {str(e)}")
            error = f"Database error: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error in RCE SQLi: {e}")
            print(f"An unexpected error occurred: {str(e)}")
            error = f"An unexpected error occurred: {str(e)}"
        finally:
            cursor.close()
            conn.close()

    return flask.render_template("blog.html", blogs=blogs, error=error, search=search)


@app.route("/sqli/rce/exec", methods=["GET"])
def sqli_rce_exec():
    """
    EXTREMELY VULNERABLE ENDPOINT - Direct Code Execution
    
    This endpoint allows direct execution of Python files - demonstrating
    the ultimate result of a successful RCE attack.
    
    WARNING: This represents complete system compromise
    Educational note: This shows why preventing SQL injection is critical,
    as it can lead to complete system takeover.
    """
    file = flask.request.args.get("file", "")
    logger.warning(f"Code execution request for file: {file}")
    
    if file:
        try:
            # EXTREMELY VULNERABLE - Direct code execution
            logger.critical(f"EXECUTING ARBITRARY CODE: {file}.py")
            exec(open(f"{file}.py").read())
            return "File executed successfully", 200
        except FileNotFoundError:
            logger.error(f"File not found: {file}.py")
            return "File not found", 404
        except Exception as e:
            logger.error(f"Error executing file {file}.py: {e}")
            return f"Error executing file: {str(e)}", 500
    else:
        return "'file' parameter is required", 400


if __name__ == "__main__":
    db.main()
    with db.get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT @@secure_file_priv, @@plugin_dir, USER(), CURRENT_USER(), SYSTEM_USER()"
            )
            result = cursor.fetchone()
            if result:
                secure_file_priv, plugin_dir, user, current_user, system_user = result
                print("Secure file priv:", secure_file_priv)
                print("Plugin dir:", plugin_dir)
                print("MySQL User:", user)
                print("Current User:", current_user)
                print("System User:", system_user)
            else:
                print("Failed to retrieve MySQL system information")

    app.run(host="0.0.0.0", port=1303)
