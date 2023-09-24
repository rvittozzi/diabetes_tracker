from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

app = Flask(__name__)

# Configurations
CSV_FILE = "diabetes_data.csv"
ENTRIES = []


def load_data():
    global ENTRIES
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            df["Date"] = pd.to_datetime(df["Date"])
            ENTRIES.extend(df.to_dict(orient="records"))
        except Exception as e:
            print(f"An error occurred while reading the CSV: {e}")


def validate_entry(date, blood_sugar):
    # Add validation logic here (e.g., date format, blood sugar range)
    return True


def add_entry(date_str, blood_sugar):
    global ENTRIES
    date = datetime.strptime(date_str, "%Y-%m-%d")
    entry = {"Date": date, "Blood Sugar (mg/dL)": blood_sugar}
    ENTRIES.append(entry)

    df = pd.DataFrame(ENTRIES)
    df.to_csv(CSV_FILE, index=False)


def plot_data():
    if not ENTRIES:
        return None
    df = pd.DataFrame(ENTRIES)
    df.set_index("Date", inplace=True)
    plt.figure(figsize=(10, 6))
    df.plot(title="Blood Sugar Tracker")
    plt.xlabel("Date")
    plt.ylabel("Blood Sugar (mg/dL)")
    plt.savefig("static/plot.png")
    return "static/plot.png"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        date_str = request.form.get("date")
        blood_sugar = float(request.form.get("blood_sugar"))

        if validate_entry(date_str, blood_sugar):
            add_entry(date_str, blood_sugar)
            return redirect(url_for("index"))

    plot_image = plot_data()
    return render_template("index.html", entries=ENTRIES, plot_image=plot_image)


@app.route("/clear_data")
def clear_data():
    global ENTRIES
    ENTRIES = []
    df = pd.DataFrame(columns=["Date", "Blood Sugar (mg/dL)"])
    df.to_csv(CSV_FILE, index=False)
    return redirect(url_for("index"))


@app.route("/previous_results")
def previous_results():
    return render_template("previous_results.html", entries=ENTRIES)


@app.route("/chart")
def chart():
    plot_image = plot_data()
    return render_template("chart.html", plot_image=plot_image)


if __name__ == "__main__":
    load_data()  # Call this only once when the app starts
    app.run(debug=True, port=3000)