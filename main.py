from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BloodSugarEntry.db'  # First database
app.config['SQLALCHEMY_BINDS'] = {
    'users': 'sqlite:///users.db'  # Second database
}
app.secret_key = "hercules"

db = SQLAlchemy(app)


# First database model
class BloodSugarEntry(db.Model):
    __tablename__ = 'blood_sugar_entry'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    blood_sugar = db.Column(db.Float, nullable=False)


# Second database model

class User(db.Model):
    __bind_key__ = 'users'  # Specify the database
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


def add_entry(date_str, blood_sugar):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    new_entry = BloodSugarEntry(date=date, blood_sugar=blood_sugar)
    db.session.add(new_entry)
    db.session.commit()


def plot_data(entries):
    if not entries:
        return None

    dates = [entry.date for entry in entries]
    blood_sugar_levels = [entry.blood_sugar for entry in entries]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, blood_sugar_levels)
    plt.title("Blood Sugar Tracker")
    plt.xlabel("Date")
    plt.ylabel("Blood Sugar (mg/dL)")
    plt.savefig("static/plot.png")
    return "static/plot.png"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "password":
            session["username"] = username
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        date_str = request.form.get("date")
        blood_sugar = float(request.form.get("blood_sugar"))

        if validate_entry(date_str, blood_sugar):
            add_entry(date_str, blood_sugar)
            return redirect(url_for("index"))

    entries = BloodSugarEntry.query.all()
    plot_image = plot_data(entries)
    return render_template("index.html", entries=entries, plot_image=plot_image)


@app.route("/clear_data")
def clear_data():
    db.session.query(BloodSugarEntry).delete()
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/previous_results")
def previous_results():
    entries = BloodSugarEntry.query.all()
    return render_template("previous_results.html", entries=entries)


@app.route("/chart")
def chart():
    entries = BloodSugarEntry.query.all()
    plot_image = plot_data(entries)
    return render_template("chart.html", plot_image=plot_image)


# Add this line to explicitly set the table name (Optional)
class BloodSugarEntry(db.Model):
    __tablename__ = 'blood_sugar_entry'
    __table_args__ = {'extend_existing': True}  # new line
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    blood_sugar = db.Column(db.Float, nullable=False)


# ... (rest of the code remains the same)

if __name__ == "__main__":
    with app.app_context():  # Explicitly providing the Flask app context (Optional)
        db.create_all()
    app.run(debug=True, port=3000)
