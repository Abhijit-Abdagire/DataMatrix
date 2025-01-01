from tkinter import Tk, Label, Button, messagebox

def show_payment_reminder_screen(root):

    root.title("Payment Reminder")
    root.geometry("600x400")

    # Center the window on the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 600) // 2
    y = (screen_height  - 400) // 2

    root.geometry(f"+{x}+{y}")

    Label(root, text="Payment Reminder", font=("Arial", 18, "bold"), pady=20).pack()
    # Label(root, text="This application is currently in a limited state.", font=("Arial", 12)).pack()
    Label(root, text="Please make the necessary payment to unlock App.", font=("Arial", 12)).pack(pady=10)
    Label(root, text="For payment details, please contact:", font=("Arial", 12)).pack()
    Label(root, text="[Mobile : 9175113022 Email : abhijit.abdagire5@gmail.com]", font=("Arial", 12)).pack(pady=10)

    # Button with hover effect
    sample_button = Button(
        root,
        text="Acknowledge",
        command=root.destroy,
        bg="#0061e0",
        fg="white",
        font=("Montserrat", 10, "bold"),
        width=16,
        height=2,
        relief="flat",
        bd=0,
    )

    # Bind events for hover effect
    sample_button.bind("<Enter>", on_enter)
    sample_button.bind("<Leave>", on_leave)

    sample_button.pack(pady=20)

    root.mainloop()

def on_enter(event):
    event.widget.config(bg="#0051b3")

def on_leave(event):
    event.widget.config(bg="#0061e0")