from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import matplotlib.pyplot as plt
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'combined.db')

app.secret_key = "hercules"

db = SQLAlchemy(app)


class BloodSugarEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    blood_sugar = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # New Field
    age = db.Column(db.Integer, nullable=False)  # New Field
    entries = db.relationship('BloodSugarEntry', backref='user', lazy=True)
    password_hash = db.Column(db.String(128))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            flash("You must be logged in to access this page.")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


def add_entry(date_str, blood_sugar, user_id):
    date = datetime.now()  # Current date and time
    new_entry = BloodSugarEntry(date=date, blood_sugar=blood_sugar, user_id=user_id)
    db.session.add(new_entry)
    db.session.commit()


def validate_entry(date_str, blood_sugar):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        float(blood_sugar)
        return True
    except ValueError:
        flash("Invalid date or blood sugar value.")
        return False


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


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")  # New Field
        age = int(request.form.get("age"))  # New Field
        hashed_password = generate_password_hash(password, method='sha256')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Choose a different one.")
        else:
            new_user = User(username=username, password_hash=hashed_password, email=email, age=age)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful. Please log in.")
            return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password_hash, password):
                session["username"] = username
                session["user_id"] = user.id
                return redirect(url_for("index"))
            else:
                flash("Invalid password")
        else:
            flash("Username does not exist")
    return render_template("login.html")


@app.route("/logout", methods=['POST'])
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        date_str = request.form.get("date")
        blood_sugar = float(request.form.get("blood_sugar"))
        user_id = session.get("user_id")
        if validate_entry(date_str, blood_sugar):
            add_entry(date_str, blood_sugar, user_id)
            return redirect(url_for("index"))
    user_id = session.get("user_id")
    entries = BloodSugarEntry.query.filter_by(user_id=user_id).all()
    plot_image = plot_data(entries)
    return render_template("index.html", entries=entries, plot_image=plot_image)


@app.route("/clear_data")
@login_required
def clear_data():
    user_id = session.get("user_id")
    BloodSugarEntry.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return redirect(url_for("index"))


@app.route('/previous_results')
@login_required
def previous_results():
    user_id = session.get("user_id")
    all_entries = BloodSugarEntry.query.filter_by(user_id=user_id).all()
    return render_template('previous_results.html', entries=all_entries)


@app.route("/chart")
@login_required
def chart():
    user_id = session.get("user_id")
    entries = BloodSugarEntry.query.filter_by(user_id=user_id).all()
    plot_image = plot_data(entries)
    return render_template("chart.html", plot_image=plot_image)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=3000)
