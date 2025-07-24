import flask
import os, time
import database.db as db
import mysql.connector
from datetime import timedelta


app = flask.Flask(__name__)
app.secret_key = os.urandom(24).hex()

app.permanent_session_lifetime = timedelta(minutes=5)

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
    error = None
    if flask.request.method == "POST":
        username = flask.request.form.get("username")
        password = flask.request.form.get("password")

        if username and password:

            conn = db.get_db_connection()
            cursor = conn.cursor(dictionary=True)

            try:
                cursor.execute(
                    f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
                )

                user = cursor.fetchall()
                if user:
                    user = user[0]
                else:
                    user = None

                print(f"User: {user}")
                if user:
                    flask.session["username"] = user.get("username")
                    if user.get("role") == "admin":
                        flask.session["secret"] = FLAG_1
                    else:
                        flask.session["secret"] = None
                    return flask.redirect("/sqli/basic/profile")
                else:
                    error = "Invalid credentials"
            except Exception:
                error = f"Internal Server Error"
            finally:
                cursor.close()
                conn.close()

    return flask.render_template("login.html", error=error)


@app.route("/sqli/union", methods=["GET"])
def sqli_union():
    blogs = []
    error = None

    search = flask.request.args.get("search", "")

    if search:

        conn = db.get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(
                f"SELECT title, author_name FROM blogs WHERE title LIKE '%{search}%'"
            )

            blogs = cursor.fetchall()
        except Exception:
            error = f"Internal Server Error"
        finally:
            cursor.close()
            conn.close()

    return flask.render_template("blog.html", blogs=blogs, error=error, search=search)


@app.route("/sqli/error", methods=["GET"])
def sqli_error():
    blogs = []
    error = None

    search = flask.request.args.get("search", "")

    if search:
        conn = db.get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(
                f"SELECT title, author_name FROM blogs WHERE title LIKE '%{search}%'"
            )

            blogs = cursor.fetchall()
        except mysql.connector.Error as e:
            error = f"Database error: {str(e)}"
        except Exception as e:
            error = f"An unexpected error occurred: {str(e)}"
        finally:
            cursor.close()
            conn.close()

    return flask.render_template("blog.html", blogs=blogs, error=error, search=search)


@app.route("/sqli/boolean", methods=["GET"])
def sqli_boolean():
    search = flask.request.args.get("search", "")
    res = "Not found"
    if search != "":

        conn = db.get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(f"SELECT * FROM users WHERE username = '{search}'")
            user = cursor.fetchall()
            if user:
                res = "Found"

            return flask.render_template(
                "user.html", search=search, result=res, show_result=True
            )
        except Exception as e:
            print("Error:", e)
            return flask.render_template(
                "user.html", search=search, result=res, show_result=True
            )
        finally:
            cursor.close()
            conn.close()

    return flask.render_template("user.html", search=search, show_result=True)


@app.route("/sqli/time", methods=["GET"])
def sqli_time():
    search = flask.request.args.get("search", "")
    if search != "":

        conn = db.get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            start = time.time()
            cursor.execute(f"SELECT * FROM users WHERE username = '{search}'")
            end = time.time()
            print("Query delay:", end - start)

            if cursor.fetchall():
                return flask.render_template("user.html", search=search, result="Found")
        except Exception as e:
            print("Error:", e)
            return flask.render_template("user.html", search=search, result="Not found")
        finally:
            cursor.close()
            conn.close()

    return flask.render_template("user.html", search=search)


@app.route("/sqli/rce", methods=["GET"])
def sqli_to_rce():
    blogs = []
    error = None

    search = flask.request.args.get("search", "")

    if search:
        conn = db.get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(
                f"SELECT title, author_name FROM blogs WHERE title LIKE '%{search}%'"
            )

            blogs = cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Database error: {str(e)}")
            error = f"Database error: {str(e)}"
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            error = f"An unexpected error occurred: {str(e)}"
        finally:
            cursor.close()
            conn.close()

    return flask.render_template("blog.html", blogs=blogs, error=error, search=search)


@app.route("/sqli/rce/exec", methods=["GET"])
def sqli_rce_exec():
    file = flask.request.args.get("file", "")
    if file:
        try:
            exec(open(f"{file}.py").read())
            return "File executed successfully", 200
        except FileNotFoundError:
            return "File not found", 404
        except Exception as e:
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
