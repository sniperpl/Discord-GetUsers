from tkinter import *
from tkinter import messagebox

import webbrowser
import requests
import time
import os

from config import UB_TITLE

def getUsers():
    auth = Authorization.get()
    if not auth:
        messagebox.showwarning(UB_TITLE, 'Enter Bot Token')
        return
    
    headers = {
        'Authorization': f'Bot {auth}'
    }

    authkey = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
    if authkey.status_code != 200:
        messagebox.showerror(UB_TITLE, "Wrong Authorization Key")
        return

    guildId = enterGuildId.get()
    if not guildId:
        messagebox.showwarning(UB_TITLE, 'Enter GuildID')
        return
    
    gid = requests.get(f'https://discord.com/api/v10/guilds/{guildId}/bans', headers=headers)
    if gid.status_code == 403:
        messagebox.showerror(UB_TITLE, "Missing Permissions.")
        return
    elif gid.status_code != 200:
        messagebox.showerror(UB_TITLE, "Bot must be on the server")
        return
    else:
        bans = gid.json()

    if not os.path.exists("botKey.txt"):
        with open("botKey.txt", "w") as file:
            file.write(auth)

    startTime = time.time()

    for unban in bans:
        userId = unban['user']['id']
        requests.delete(f"https://discord.com/api/v10/guilds/{guildId}/bans/{userId}", headers=headers)
        time.sleep(.3)

    messagebox.showinfo(UB_TITLE, f'Unbanned {len(bans)} users in {time.time() - startTime:.0f}s')
    return

# Tworzenie głównego okna aplikacji
def guiUnbanAll(root):
    global Authorization, enterGuildId, labels

    root.title(UB_TITLE)

    labels = []
    containerFrame = Frame(root)
    labels.append(containerFrame)

    label_Authorization = Label(containerFrame, text="Authorization")
    label_Authorization.pack(pady=(30,0))
    button_Authorization = Button(containerFrame, text="Where Can I Find Bot Token?", command=lambda: webbrowser.open("https://youtu.be/54d0mquJqAc"), relief="flat", bg=containerFrame.cget("bg"), fg="blue", font=("Arial", 8, "underline"), bd=0)
    button_Authorization.pack()
    Authorization = Entry(containerFrame)
    Authorization.pack(pady=(1,0))

    if os.path.exists("botKey.txt"):
        with open("botKey.txt", "r") as file:
            botKey = file.read()
            Authorization.insert(0, botKey)

    label_guildId = Label(containerFrame, text="GuildID")
    label_guildId.pack(pady=(10,0))
    enterGuildId = Entry(containerFrame)
    enterGuildId.pack()

    submitButton = Button(containerFrame, text="Unban", command=getUsers)
    submitButton.pack(pady=(20,0))

    containerFrame.pack()

def hideUnbanAll():
    for label in labels:
        label.pack_forget()
