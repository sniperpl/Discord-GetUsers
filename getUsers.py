import tkinter as tk
from tkinter import ttk, messagebox

from users import guiUsers, hideUsersFile
from usersToMsgID import guiUsersMsgID, hideUsersFileMsgID

def onChoose(event):
    options = {
        "Get Users": guiUsers,
        "Get Users to msgid": guiUsersMsgID
    }

    selected_option = combobox.get()

    if selected_option in options:
        options[selected_option](root)
        hideWidgets()
    else:
        messagebox.showerror("ERROR", f"Nieobsługiwana opcja: {selected_option}")

def hideWidgets():
    label_option.pack_forget()
    combobox.pack_forget()
    button_back.place(x=10, y=10)

def showWidgets():
    label_option.pack(pady=(150,0))
    combobox.pack(pady=(5,0))
    button_back.place_forget()
    if combobox.get() == "Get Users":
        hideUsersFile()
    elif combobox.get() == "Get Users to msgid":
        hideUsersFileMsgID()
    root.title("App")

root = tk.Tk()
root.title("App")
root.geometry("500x350")

label_option = tk.Label(root, text="Choose Option")
label_option.pack(pady=(150,0))

options = ["Get Users", "Get Users to msgid"]
combobox = ttk.Combobox(root, values=options, state="readonly")
combobox.pack(pady=(5,0))
combobox.bind("<<ComboboxSelected>>", onChoose)

button_back = tk.Button(root, text=" ❮ ", command=showWidgets)

root.mainloop()