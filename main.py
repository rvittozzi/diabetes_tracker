import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import tkinter as tk
from tkinter import ttk


# Initialize an empty list to store entries
entries = []

# Initialize a tkinter window
root = tk.Tk()
root.title("Diabetes Tracker")

# Function to add a new entry
def add_entry():
    date_str = date_entry.get()
    blood_sugar = float(blood_sugar_entry.get())
    date = datetime.strptime(date_str, "%Y-%m-%d")
    entry = {"Date": date, "Blood Sugar (mg/dL)": blood_sugar}
    entries.append(entry)
    update_entries_list()
    date_entry.delete(0, "end")
    blood_sugar_entry.delete(0, "end")
    status_label.config(text="Entry added successfully!")

# Function to update the entries list in the GUI
def update_entries_list():
    entries_list.delete(0, "end")
    for entry in entries:
        entries_list.insert("end", f"{entry['Date']} - {entry['Blood Sugar (mg/dL)']}")

# Function to plot the data
def plot_data():
    if not entries:
        status_label.config(text="No data to plot.")
        return
    df = pd.DataFrame(entries)
    df.set_index("Date", inplace=True)
    df.plot(title="Blood Sugar Tracker")
    plt.xlabel("Date")
    plt.ylabel("Blood Sugar (mg/dL)")
    plt.show()

# Create and configure GUI elements
date_label = ttk.Label(root, text="Enter the date (YYYY-MM-DD):")
date_entry = ttk.Entry(root)
blood_sugar_label = ttk.Label(root, text="Enter the blood sugar level (mg/dL):")
blood_sugar_entry = ttk.Entry(root)
add_button = ttk.Button(root, text="Add Entry", command=add_entry)
entries_list = tk.Listbox(root, width=50, height=10)
plot_button = ttk.Button(root, text="Plot Data", command=plot_data)
status_label = ttk.Label(root, text="")

# Arrange GUI elements using grid layout
date_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
date_entry.grid(row=0, column=1, padx=10, pady=5)
blood_sugar_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
blood_sugar_entry.grid(row=1, column=1, padx=10, pady=5)
add_button.grid(row=2, column=0, columnspan=2, pady=10)
entries_list.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
plot_button.grid(row=4, column=0, columnspan=2, pady=10)
status_label.grid(row=5, column=0, columnspan=2, pady=5)

# Start the GUI main loop
root.mainloop()