import tkinter as tk
from tkinter import filedialog
from src.ui.navigation import switch_screen
from src.logic.common_utils import save_settings,read_setting


def create_settings_screen(root):
    switch_screen(root, lambda root: _settings_screen_content(root))


def on_enter(event):
    event.widget.config(bg="#0041b3")


def on_leave(event):
    event.widget.config(bg="#0061e0")


def _settings_screen_content(root):
    root.title("Settings Screen")
    root.geometry("600x400")

    # Excel File Path
    tk.Label(root, text="Excel File Path:").grid(row=0, column=0, padx=2, pady=10, sticky="w")
    excel_path_entry = tk.Entry(root, width=50)
    excel_path_entry.insert(0, read_setting("excel_file_path"))
    excel_path_entry.grid(row=0, column=1, padx=2, pady=10)

    def browse_excel_file():
        path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls;*.xlsm;*.xlsb;*.xltm;*.xltx")])
        excel_path_entry.delete(0, tk.END)
        excel_path_entry.insert(0, path)

    browse_excel_button = tk.Button(
        root,
        text="Browse",
        command=browse_excel_file,
        bg="#0061e0",
        fg="white",
        font=("Montserrat", 9, "bold"),
        width=12,
        height=1,
        relief="flat",
        bd=0,
    )
    browse_excel_button.bind("<Enter>", on_enter)
    browse_excel_button.bind("<Leave>", on_leave)
    browse_excel_button.grid(row=0, column=2, padx=2, pady=10)

    # Output Directory Path
    tk.Label(root, text="Output Directory Path:").grid(row=1, column=0, padx=2, pady=10, sticky="w")
    output_path_entry = tk.Entry(root, width=50)
    output_path_entry.insert(0, read_setting("output_dir_path"))
    output_path_entry.grid(row=1, column=1, padx=2, pady=10)

    def browse_output_dir():
        path = filedialog.askdirectory()
        output_path_entry.delete(0, tk.END)
        output_path_entry.insert(0, path)

    browse_output_button = tk.Button(
        root,
        text="Browse",
        command=browse_output_dir,
        bg="#0061e0",
        fg="white",
        font=("Montserrat", 9, "bold"),
        width=12,
        height=1,
        relief="flat",
        bd=0,
    )
    browse_output_button.bind("<Enter>", on_enter)
    browse_output_button.bind("<Leave>", on_leave)
    browse_output_button.grid(row=1, column=2, padx=2, pady=10)


    # Save and Back Buttons
    def save():
        save_settings(
            excel_file_path=excel_path_entry.get(),
            output_dir_path=output_path_entry.get()
        )

        # Defer the import to avoid circular dependency
        from src.ui.home_screen import create_home_screen

        switch_screen(root, create_home_screen)

    def go_back():
        # Defer the import to avoid circular dependency
        from src.ui.home_screen import create_home_screen

        switch_screen(root, create_home_screen)

    save_button = tk.Button(
        root,
        text="Save",
        command=save,
        bg="#0061e0",
        fg="white",
        font=("Montserrat", 10, "bold"),
        width=14,
        height=2,
        relief="flat",
        bd=0,
    )
    save_button.bind("<Enter>", on_enter)
    save_button.bind("<Leave>", on_leave)
    save_button.grid(row=3, column=0, padx=2, pady=10)

    back_button = tk.Button(
        root,
        text="Back",
        command=go_back,
        bg="#0061e0",
        fg="white",
        font=("Montserrat", 10, "bold"),
        width=14,
        height=2,
        relief="flat",
        bd=0,
    )
    back_button.bind("<Enter>", on_enter)
    back_button.bind("<Leave>", on_leave)
    back_button.grid(row=3, column=1, padx=2, pady=10)
