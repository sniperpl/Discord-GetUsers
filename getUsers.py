import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from users import guiUsers
from users import hideUsersFile

def onChoose(event):
    selected_option = combobox.get()

    if selected_option == "Get Users":
        guiUsers(root)
        hideWidgets()
    else:
        messagebox.showerror("ERROR", f"Nieobsługiwana opcja: {selected_option}")

def hideWidgets():
    label_option.pack_forget()
    combobox.pack_forget()
    button_back.place(x=10, y=10)

def showWidgets():
    label_option.pack(pady=(100,0))
    combobox.pack(pady=(5,0))
    button_back.place_forget()
    hideUsersFile()

root = tk.Tk()
root.title("App")
root.geometry("400x300")

label_option = tk.Label(root, text="Choose Option")
label_option.pack(pady=(100,0))

options = ["Get Users"]
combobox = ttk.Combobox(root, values=options, state="readonly")
combobox.pack(pady=(5,0))
combobox.bind("<<ComboboxSelected>>", onChoose)

button_back = tk.Button(root, text=" ❮ ", command=showWidgets)

root.mainloop()