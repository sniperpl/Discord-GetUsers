from tkinter import Tk

root = Tk()
root.geometry("400x450")

WINDOW_TITLE = "Get Users"
UB_TITLE = "Unban All"

def setTitle(suffix=""):
    root.title(f"{WINDOW_TITLE}{f' {suffix}' if suffix else ''}")