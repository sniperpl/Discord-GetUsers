from tkinter import ttk, messagebox, Button, Label

from src.usersByBot import guiUsers, hideUsersFile
from src.usersByUser import guiUsersClassic, hideUsersFileClassic
from src.usersToMsgID import guiUsersMsgID, hideUsersFileMsgID
from src.usersToMsgIDByBot import guiUsersMsgIDByBot, hideUsersFileMsgIDByBot
from src.usersUnbanAll import guiUnbanAll, hideUnbanAll

from config import setTitle, WINDOW_TITLE, root

def onChoose(event):
    global userHideGui

    options = {
        "By User": (guiUsersClassic, hideUsersFileClassic),
        "By Bot": (guiUsers, hideUsersFile),
        "To MsgID": (guiUsersMsgID, hideUsersFileMsgID),
        "To MsgID By Bot": (guiUsersMsgIDByBot, hideUsersFileMsgIDByBot),
        "Unban All": (guiUnbanAll, hideUnbanAll)
    }
    
    selected_option = combobox.get()
    
    if selected_option in options:
        userGui, userHideGui = options[selected_option]
        userGui(root)
        hideWidgets()
    else:
        messagebox.showerror(WINDOW_TITLE, f"Nieobsługiwana opcja: {selected_option}")

def hideWidgets():
    label_option.pack_forget()
    combobox.pack_forget()
    button_back.place(x=10, y=10)

    if combobox.get() != "Unban All":
        setTitle(combobox.get())

def showWidgets():
    label_option.pack(pady=(225,0))
    combobox.pack(pady=(5,0))
    button_back.place_forget()
    setTitle()

    globals().get('userHideGui', lambda: None)()

label_option = Label(root, text="Choose Option")

options = ["By User", "By Bot", "To MsgID", "To MsgID By Bot", "Unban All"]
combobox = ttk.Combobox(root, values=options, state="readonly")
combobox.bind("<<ComboboxSelected>>", onChoose)

button_back = Button(root, text=" ❮ ", command=showWidgets)

showWidgets()
root.mainloop()