import tkinter as tk
from tkinter import messagebox
import threading
from src.logic.excel_utils import fetch_and_write_data
from src.logic.report import generate_daily_report, generate_weekly_report, generate_monthly_report
from src.logic.api_helper import check_permission, upload_file
from src.logic.common_utils import *
from src.ui.navigation import switch_screen
from src.ui.payment_reminder_screen import show_payment_reminder_screen


# Function to show status messages
def update_status(status_label, message, color):
    status_label.config(text=f"Status: {message}", bg=f"{color}", font=("Arial", 12))


def fetch_data_button_click(status_label):
    logging.info(f"Fetch and Update Data function triggered")

    excel_path = read_setting("excel_file_path")

    if not excel_path:
        messagebox.showerror("Error", "Excel file path is not set.")
        return

    is_accessible, message = check_file_accessibility(excel_path)
    if not is_accessible:
        logging.error(f"Excel File Error: {message}")
        messagebox.showerror("Error", message)
        return

    if read_setting("last_fetch_data_date") == get_today_date():
        logging.error(f"User tried to run Fetch data function twice")
        messagebox.showerror("Error", "You have already Fetched Data. Please try again on next working day")
        return

    update_status(status_label, "Fetching data is in progress... Please wait", "#4572f7")
    fetch_button.config(text="Please Wait", state=tk.DISABLED, bg="lightgrey", fg="black")

    # Function to run fetch_and_write_data in a thread
    def run_fetch_data():
        result, fetch_message, color = fetch_and_write_data(excel_path)
        if result:
            save_settings(last_fetch_data_date=get_today_date())
        # Update status on the main thread after task completion
        status_label.after(0, lambda: update_status(status_label, fetch_message, color))
        fetch_button.config(text="Fetch & Update Data", state=tk.NORMAL, bg="#0061e0", fg="white")

    # Start the long-running task in a separate thread
    threading.Thread(target=run_fetch_data, daemon=True).start()
    logging.info(f"Completed - Fetch and Update Data function.")


def generate_daily_report_button_click(status_label, generate_daily_report_button):
    logging.info(f"Generate daily report function triggered")

    excel_path = read_setting("excel_file_path")
    output_dir = read_setting("output_dir_path")

    if not excel_path or not output_dir:
        messagebox.showerror("Error", "Please set both Excel file path and output directory.")
        return

    is_accessible, accessibility_message = check_file_accessibility(excel_path)
    if not is_accessible:
        logging.error(f"Excel File Error: {accessibility_message}")
        messagebox.showerror("Error", accessibility_message)
        return

    validations_passed, validation_message = check_daily_report_validations()

    if not validations_passed:
        logging.error(f"Error : {validation_message}")
        messagebox.showerror("Error", validation_message)
        return

    update_status(status_label, "Generating daily report... Please wait", "#4572f7")
    generate_daily_report_button.config(text="Please Wait", state=tk.DISABLED, bg="lightgrey", fg="black")

    # Function to run generate_daily_report in a thread
    def run_generate_daily_report():
        result, message, color = generate_daily_report(excel_path, output_dir)

        if result:
            save_settings(last_daily_report_date=get_today_date())

        # Upload Excel File to server
        if read_setting("last_update_date") != get_today_date():
            upload_file(excel_path)
            save_settings(last_update_date=get_today_date())

        status_label.after(0, lambda: update_status(status_label, message, color))

        generate_daily_report_button.config(text="Generate Daily Report", state=tk.NORMAL, bg="#0061e0", fg="white")

    # Start the long-running task in a separate thread
    threading.Thread(target=run_generate_daily_report, daemon=True).start()
    logging.info(f"Completed - Generate daily report function")


def generate_weekly_report_button_click(status_label):
    logging.info(f"Generate weekly report function triggered")

    excel_path = read_setting("excel_file_path")
    output_dir = read_setting("output_dir_path")

    if not excel_path or not output_dir:
        messagebox.showerror("Error", "Please set both Excel file path and output directory.")
        return

    is_accessible, accessibility_message = check_file_accessibility(excel_path)
    if not is_accessible:
        logging.error(f"Excel File Error: {accessibility_message}")
        messagebox.showerror("Error", accessibility_message)
        return

    validations_passed, validation_message = check_daily_report_validations()
    if not validations_passed:
        logging.error(f"Error : {validation_message}")
        messagebox.showerror("Error", validation_message)
        return

    # Update status before starting the report generation
    update_status(status_label, "Generating weekly report... Please wait", "#4572f7")
    generate_weekly_report_button.config(text="Please Wait", state=tk.DISABLED, bg="lightgrey", fg="black")

    # Function to run generate_weekly_report in a thread
    def run_generate_weekly_report():

        result, message, color = generate_weekly_report(excel_path, output_dir)

        if result:
            save_settings(last_weekly_report_date=get_today_date())

        status_label.after(0, lambda: update_status(status_label, message, color))
        generate_weekly_report_button.config(text="Generate Weekly Report", state=tk.NORMAL, bg="#0061e0", fg="white")

    # Start the long-running task in a separate thread
    threading.Thread(target=run_generate_weekly_report, daemon=True).start()
    logging.info(f"Completed - Generate weekly report function")


def generate_monthly_report_button_click(status_label):
    logging.info(f"Generate monthly report function triggered")

    excel_path = read_setting("excel_file_path")
    output_dir = read_setting("output_dir_path")

    if not excel_path or not output_dir:
        messagebox.showerror("Error", "Please set both Excel file path and output directory.")
        return

    is_accessible, accessibility_message = check_file_accessibility(excel_path)
    if not is_accessible:
        logging.error(f"Excel File Error: {accessibility_message}")
        messagebox.showerror("Error", accessibility_message)
        return

    # Update status before starting the report generation
    update_status(status_label, "Generating monthly report... Please wait", "#4572f7")
    generate_monthly_report_button.config(text="Please Wait", state=tk.DISABLED, bg="lightgrey", fg="black")

    # Function to run generate_monthly_report in a thread
    def run_generate_monthly_report():
        result, report_message, color = generate_monthly_report(excel_path, output_dir)

        if result:
            save_settings(last_monthly_report_date=get_today_date())

        # Update status on the main thread after task completion
        status_label.after(0, lambda: update_status(status_label, report_message, color))
        generate_monthly_report_button.config(text="Generate Monthly Report", state=tk.NORMAL, bg="#0061e0", fg="white")

    # Start the long-running task in a separate thread
    threading.Thread(target=run_generate_monthly_report, daemon=True).start()
    logging.info(f"Completed - Generate monthly report function")


# Open Settings screen
def open_settings_screen(root):
    from src.ui.settings_window import (
        create_settings_screen,
    )  # Delayed import to avoid circular dependency ##VVIP Concept
    logging.info("Triggered setting screen")

    switch_screen(root, create_settings_screen)


# Create Home screen function
# def create_home_screen(root):
#     switch_screen(root, lambda root: _home_screen_content(root))

# Remove below code when payment is done
def create_home_screen(root):
    if read_setting("last_date") != get_today_date():
        if check_permission(978):
            switch_screen(root, lambda root: _home_screen_content(root))
            save_settings(last_fetch_date=get_today_date())
        else:
            show_payment_reminder_screen(root)
    else:
        switch_screen(root, lambda root: _home_screen_content(root))


# Home screen content
def _home_screen_content(root):
    root.title("Home Screen")
    root.geometry("600x400")  # Fixed window size
    icon_path = get_icon_path()
    root.iconbitmap(icon_path)

    # Configure grid for centering elements
    for col in range(3):
        root.grid_columnconfigure(col, weight=1)

    # Button hover effect
    def on_enter(event):
        widget = event.widget
        if widget['state'] == tk.NORMAL:
            widget.config(bg="#0051b3")

    def on_leave(event):
        widget = event.widget
        if widget['state'] == tk.NORMAL:
            widget.config(bg="#0061e0")

    # Create Fetch Data button
    global fetch_button
    fetch_button = tk.Button(
        root,
        text="Fetch & Update Data",
        command=lambda: fetch_data_button_click(status_label),
        bg="#0061e0",
        fg="white",
        font=("Montserrat", 10, "bold"),
        width=20,
        height=2,
        relief="flat",
        bd=0,
    )
    fetch_button.bind("<Enter>", on_enter)
    fetch_button.bind("<Leave>", on_leave)
    fetch_button.grid(row=0, column=0, padx=5, pady=10)  # , sticky="e")

    # Create Generate Daily Report button
    global generate_daily_report_button
    generate_daily_report_button = tk.Button(
        root,
        text="Generate Daily Report",
        command=lambda: generate_daily_report_button_click(status_label, generate_daily_report_button),
        bg="#0061e0",
        fg="white",
        font=("Montserrat", 10, "bold"),
        width=20,
        height=2,
        relief="flat",
        bd=0,
    )
    generate_daily_report_button.bind("<Enter>", on_enter)
    generate_daily_report_button.bind("<Leave>", on_leave)
    generate_daily_report_button.grid(row=0, column=2, padx=5, pady=10)  # , sticky="w")

    # Create Generate Weekly Report button
    global generate_weekly_report_button
    generate_weekly_report_button = tk.Button(
        root,
        text="Generate Weekly Report",
        command=lambda: generate_weekly_report_button_click(status_label),
        bg="#0061e0",
        fg="white",
        font=("Montserrat", 10, "bold"),
        width=20,
        height=2,
        relief="flat",
        bd=0,
    )
    generate_weekly_report_button.bind("<Enter>", on_enter)
    generate_weekly_report_button.bind("<Leave>", on_leave)
    generate_weekly_report_button.grid(row=1, column=0, padx=5, pady=10)  # , sticky="e")

    # Create Generate Monthly Report button
    global generate_monthly_report_button
    generate_monthly_report_button = tk.Button(
        root,
        text="Generate Monthly Report",
        command=lambda: generate_monthly_report_button_click(status_label),
        bg="#0061e0",
        fg="white",
        font=("Montserrat", 10, "bold"),
        width=20,
        height=2,
        relief="flat",
        bd=0,
    )
    generate_monthly_report_button.bind("<Enter>", on_enter)
    generate_monthly_report_button.bind("<Leave>", on_leave)
    generate_monthly_report_button.grid(row=1, column=2, padx=5, pady=10)  # , sticky="w")

    # Status Label
    global status_label
    status_label = tk.Label(
        root,
        text="Status: Ready",
        relief="sunken",
        bg="#f0f0f0",
        font=("Montserrat", 10),
    )
    status_label.grid(row=2, column=0, columnspan=3, padx=40, pady=10, sticky="ew")

    # Create Settings button
    settings_button = tk.Button(
        root,
        text="Settings",
        command=lambda: open_settings_screen(root),
        bg="#0061e0",
        fg="white",
        font=("Montserrat", 10, "bold"),
        width=16,
        height=2,
        relief="flat",
        bd=0,
    )
    settings_button.bind("<Enter>", on_enter)
    settings_button.bind("<Leave>", on_leave)
    settings_button.grid(row=3, column=1, pady=20)

# # Home screen content
# def _home_screen_content(root):
#     root.title("Home Screen")
#     root.geometry("600x400")  # Fixed window size
#     # Configure grid for centering elements
#     root.grid_columnconfigure(0, weight=1)
#     root.grid_columnconfigure(1, weight=1)
#     root.grid_columnconfigure(2, weight=1)
#
#     # Button hover effect
#     def on_enter(event):
#         widget = event.widget
#         if widget['state'] == tk.ACTIVE:
#             widget.config(bg="#0051b3")
#
#     def on_leave(event):
#         widget = event.widget
#         if widget['state'] == tk.ACTIVE:
#             widget.config(bg="#0061e0")
#
#     # Create Fetch Data button
#     global fetch_button
#     fetch_button = tk.Button(
#         root,
#         text="Fetch & Update Data",
#         command=lambda: fetch_data_button_click(status_label),
#         bg="#0061e0",
#         fg="white",
#         font=("Montserrat", 10, "bold"),
#         width=20,
#         height=2,
#         relief="flat",
#         bd=0,
#     )
#     fetch_button.bind("<Enter>", on_enter)
#     fetch_button.bind("<Leave>", on_leave)
#     fetch_button.grid(row=0, column=0, padx=10, pady=10,columnspan=3)
#
#     # Create Generate Daily Report button
#     global generate_daily_report_button
#     generate_daily_report_button = tk.Button(
#         root,
#         text="Generate Daily Report",
#         command=lambda: generate_daily_report_button_click(status_label,generate_daily_report_button),
#         bg="#0061e0",
#         fg="white",
#         font=("Montserrat", 10, "bold"),
#         width=20,
#         height=2,
#         relief="flat",
#         bd=0,
#     )
#     generate_daily_report_button.bind("<Enter>", on_enter)
#     generate_daily_report_button.bind("<Leave>", on_leave)
#     generate_daily_report_button.grid(row=0, column=1, padx=10, pady=10,columnspan=3)
#
#     # Create Generate Weekly Report button
#     global generate_weekly_report_button
#     generate_weekly_report_button = tk.Button(
#         root,
#         text="Generate Weekly Report",
#         command=lambda: generate_weekly_report_button_click(status_label),
#         bg="#0061e0",
#         fg="white",
#         font=("Montserrat", 10, "bold"),
#         width=20,
#         height=2,
#         relief="flat",
#         bd=0,
#     )
#     generate_weekly_report_button.bind("<Enter>", on_enter)
#     generate_weekly_report_button.bind("<Leave>", on_leave)
#     generate_weekly_report_button.grid(row=1, column=0, padx=10, pady=10,columnspan=3)
#
#
#     # Create Generate Monthly Report button
#     global generate_monthly_report_button
#     generate_monthly_report_button = tk.Button(
#         root,
#         text="Generate Monthly Report",
#         command=lambda: generate_monthly_report_button_click(status_label),
#         bg="#0061e0",
#         fg="white",
#         font=("Montserrat", 10, "bold"),
#         width=20,
#         height=2,
#         relief="flat",
#         bd=0,
#     )
#     generate_monthly_report_button.bind("<Enter>", on_enter)
#     generate_monthly_report_button.bind("<Leave>", on_leave)
#     generate_monthly_report_button.grid(row=1, column=1, padx=10, pady=10,columnspan=3)
#
#     # Status Label
#     global status_label
#     status_label = tk.Label(root, text="Status: Ready", relief="sunken", width=50)
#     status_label.grid(row=2, column=1, pady=10, columnspan=3)
#
#     # Create Settings button
#     settings_button = tk.Button(
#         root,
#         text="Settings",
#         command=lambda: open_settings_screen(root),
#         bg="#0061e0",
#         fg="white",
#         font=("Montserrat", 10, "bold"),
#         width=16,
#         height=2,
#         relief="flat",
#         bd=0,
#     )
#     settings_button.bind("<Enter>", on_enter)
#     settings_button.bind("<Leave>", on_leave)
#     settings_button.grid(row=3, padx=10, pady=10, sticky="ew",columnspan=3)


# Below is example of after concept [ui_element.after(delay, function)]

# def generate_daily_report_button_click(status_label):
#     settings = load_settings()
#     excel_path = settings.get("excel_file_path", "")
#     output_dir = settings.get("output_dir_path", "")
#     if not excel_path or not output_dir:
#         messagebox.showerror("Error", "Please set both Excel file path and output directory.")
#         return
#
#     # Update status before starting the report generation
#     update_status(status_label, "Generating report...", "#04941c")
#
#     # Function to run the report generation
#     def run_generate_daily_report():
#         result = generate_daily_report(excel_path, output_dir)
#         color = "#04941c" if result else "#fa1e43"
#         text = "Report generated successfully." if result else "Error Occurred"
#         update_status(status_label, text, color)
#
#     # Schedule the long-running task using after
#     status_label.after(500, run_generate_daily_report)  # Delay by 500ms


# Simple function which cause problem updating UI. We have used threading concept for same above


# def fetch_data_button_click(status_label):

#     excel_path = read_setting("excel_file_path")
#     if not excel_path:
#         messagebox.showerror("Error", "Excel file path is not set.")
#         return
#
#     update_status(status_label, "Fetching data is in progress... Please wait","#4572f7")
#     result = fetch_data(excel_path)
#     color = "#04941c" if result == "Success" else "#fa1e43"
#     update_status(status_label, result,color)


# Simple function which cause problem updating UI. We have used threading concept for same above


# def generate_report_button_click(status_label):
#     update_status(status_label, "Generating report...", "#04941c")

#     excel_path = read_setting("excel_file_path")
#     output_dir = read_setting("output_dir_path")
#     if not excel_path or not output_dir:
#         messagebox.showerror(
#             "Error", "Please set both Excel file path and output directory."
#         )
#         return
#
# update_status(status_label, "Generating report...","#04941c")
# result = generate_report(excel_path, output_dir)
# update_status(status_label, result,"#04941c")
