import tkinter as tk
from src.ui.home_screen import create_home_screen
from src.logic.common_utils import configure_logging

if __name__ == "__main__":
    root = tk.Tk()
    configure_logging()
    create_home_screen(root)
    root.mainloop()