from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import threading
import time
from plyer import notification
from diabetes_utils import get_last_check_time
from diabetes_data_module import get_blood_sugar_data_from_csv

app = Flask(__name__)

# Initialize the CSV file path
csv_file = "diabetes_data.csv"

# Initialize an empty list to store entries
entries = []

# Function to load existing data from the CSV file
def load_data():
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        df["Date"] = pd.to_datetime(df["Date"])
        entries.extend(df.to_dict(orient="records"))

# Function to add a new entry
def add_entry():
    global entries
    if request.method == "POST":
        date_str = request.form.get("date")
        blood_sugar = float(request.form.get("blood_sugar"))
        date = datetime.strptime(date_str, "%Y-%m-%d")
        entry = {"Date": date, "Blood Sugar (mg/dL)": blood_sugar}
        entries.append(entry)

        # Save the entry to the CSV file
        df = pd.DataFrame(entries)
        df.to_csv(csv_file, index=False)

    return redirect(url_for("index"))

# Function to plot the data
def plot_data():
    if not entries:
        return None
    df = pd.DataFrame(entries)
    df.set_index("Date", inplace=True)
    plt.figure(figsize=(10, 6))
    df.plot(title="Blood Sugar Tracker")
    plt.xlabel("Date")
    plt.ylabel("Blood Sugar (mg/dL)")
    plt.savefig("static/plot.png")
    return "static/plot.png"

# Function to check blood sugar and send notifications
def check_blood_sugar():
    while True:
        blood_sugar_data = get_blood_sugar_data_from_csv(csv_file)  # Get blood sugar data from the CSV
        last_check_time = get_last_check_time()  # Get the last check time from the module

        # ... Your existing code for notifications and reminders ...

        time.sleep(3600)  # Repeat every hour

# Create a separate thread for the reminder logic
reminder_thread = threading.Thread(target=check_blood_sugar)
reminder_thread.daemon = True
reminder_thread.start()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return add_entry()
    load_data()
    plot_image = plot_data()  # Get the plot image filename
    return render_template("index.html", entries=entries, plot_image=plot_image)

@app.route("/clear_data")
def clear_data():
    global entries
    entries = []
    # Clear the CSV file by overwriting it with an empty DataFrame
    df = pd.DataFrame(columns=["Date", "Blood Sugar (mg/dL)"])
    df.to_csv(csv_file, index=False)
    return redirect(url_for("index"))

@app.route("/previous_results")
def previous_results():
    load_data()  # Load the data
    return render_template("previous_results.html", entries=entries)

if __name__ == "__main__":
    load_data()  # Call load_data to load existing data
    app.run(debug=True, port=3000)