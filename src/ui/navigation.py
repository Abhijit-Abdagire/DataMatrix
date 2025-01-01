def switch_screen(root, new_screen_function):
    """Clears the current screen and loads a new one."""
    for widget in root.winfo_children():
        widget.destroy()
    new_screen_function(root)