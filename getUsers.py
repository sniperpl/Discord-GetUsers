from tkinter import *
from tkinter import ttk, messagebox

from users import guiUsers, hideUsersFile
from usersToMsgID import guiUsersMsgID, hideUsersFileMsgID
from usersByUser import guiUsersClassic, hideUsersFileClassic
from usersUnbanAll import guiUnbanAll, hideUnbanAll

def onChoose(event):
    global userHideGui

    options = {
        "By you": (guiUsersClassic, hideUsersFileClassic),
        "By bot": (guiUsers, hideUsersFile),
        "To msgid": (guiUsersMsgID, hideUsersFileMsgID),
        "UnbanAll": (guiUnbanAll, hideUnbanAll)
    }
    
    selected_option = combobox.get()
    
    if selected_option in options:
        userGui, userHideGui = options[selected_option]
        userGui(root)
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
    root.title("Get Users")

    userHideGui = globals().get('userHideGui', lambda: None)
    userHideGui()

root = Tk()
root.geometry("400x450")

label_option = Label(root, text="Choose Option")

options = ["By you", "By bot", "To msgid", "UnbanAll"]
combobox = ttk.Combobox(root, values=options, state="readonly")
combobox.bind("<<ComboboxSelected>>", onChoose)

button_back = Button(root, text=" ❮ ", command=showWidgets)

showWidgets()

root.mainloop()