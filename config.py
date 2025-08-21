from tkinter import Tk

verApi = "v10"
defFont = "Bahnschrift Light"
WINDOW_TITLE = "Get Users"
UB_TITLE = "Unban All"

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")

root = Tk()
center_window(root, 400, 500)

root.iconbitmap("favicon.ico")
root.option_add("*Label.Font", (defFont, 13))
root.option_add("*Entry.Width", 25)

def setTitle(suffix=""):
    root.title(f"{WINDOW_TITLE}{f' {suffix}' if suffix else ''}")