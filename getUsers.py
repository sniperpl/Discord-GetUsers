import tkinter as tk
from tkinter import ttk, messagebox

from users import guiUsers, hideUsersFile
from usersToMsgID import guiUsersMsgID, hideUsersFileMsgID
from usersByUser import guiUsersClassic, hideUsersFileClassic
from usersUnbanAll import guiUnbanAll, hideUnbanAll

def onChoose(event):
    options = {
        "By you": guiUsersClassic,
        "By bot": guiUsers,
        "To msgid": guiUsersMsgID,
        "UnbanAll": guiUnbanAll
    }

    selected_option = combobox.get()

    if selected_option in options:
        options[selected_option](root)
        hideWidgets()
    else:
        messagebox.showerror("Get Users", f"Nieobsługiwana opcja: {selected_option}")

def hideWidgets():
    label_option.pack_forget()
    combobox.pack_forget()
    button_back.place(x=10, y=10)

def showWidgets():
    label_option.pack(pady=(200,0))
    combobox.pack(pady=(5,0))
    button_back.place_forget()
    root.title("App")

    options = {
        "By you": hideUsersFileClassic,
        "By bot": hideUsersFile,
        "To msgid": hideUsersFileMsgID,
        "UnbanAll": hideUnbanAll
    }
    options.get(combobox.get())()

root = tk.Tk()
root.title("App")
root.geometry("400x450")

label_option = tk.Label(root, text="Choose Option")
label_option.pack(pady=(200,0))

options = ["By you", "By bot", "To msgid", "UnbanAll"]
combobox = ttk.Combobox(root, values=options, state="readonly")
combobox.pack(pady=(5,0))
combobox.bind("<<ComboboxSelected>>", onChoose)

button_back = tk.Button(root, text=" ❮ ", command=showWidgets)

root.mainloop()