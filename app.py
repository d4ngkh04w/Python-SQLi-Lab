import flask
import os
import database.db as db
import mysql.connector
import dotenv
from datetime import timedelta

dotenv.load_dotenv()
app = flask.Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24).hex())
app.permanent_session_lifetime = timedelta(minutes=5)


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
            try:
                conn = db.get_db_connection()
                cursor = conn.cursor(dictionary=True)
                cursor.execute(
                    f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
                )
                user = cursor.fetchone()
                conn.close()
                if user:
                    flask.session["username"] = user.get("username")
                    flask.session["secret"] = user.get("secret")
                    return flask.redirect("/sqli/basic/profile")
                else:
                    error = "Invalid credentials"
            except Exception as e:
                error = f"Internal Server Error"
    else:
        flask.session.clear()
    return flask.render_template("login.html", error=error)


@app.route("/sqli/union", methods=["GET"])
def sqli_union():
    blogs = []
    error = None

    search = flask.request.args.get("search", "")

    if search:
        try:
            conn = db.get_db_connection()
            cursor = conn.cursor(dictionary=True)

            query = (
                f"SELECT title, author_name FROM blogs WHERE title LIKE '%{search}%'"
            )

            cursor.execute(query)
            blogs = cursor.fetchall()
            conn.close()
        except Exception as e:
            error = f"Internal Server Error"

    return flask.render_template("blog.html", blogs=blogs, error=error, search=search)


if __name__ == "__main__":
    db.main()
    app.run(host="0.0.0.0", port=1303)
