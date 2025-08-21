import tkinter as tk
from tkinter import messagebox

import webbrowser, requests, time, os

from config import root, verApi, defFont, UB_TITLE, center_window

def getUsers():
    auth = Authorization.get()
    if not auth:
        messagebox.showwarning(UB_TITLE, "Enter Bot Token")
        return
    
    headers = {
        "Authorization": f"Bot {auth}"
    }

    authkey = requests.get(f"https://discord.com/{verApi}/v10/users/@me", headers=headers)
    if authkey.status_code != 200:
        messagebox.showerror(UB_TITLE, "Wrong Authorization Key")
        return

    guildId = enterGuildId.get()
    if not guildId:
        messagebox.showwarning(UB_TITLE, "Enter GuildID")
        return
    
    gid = requests.get(f"https://discord.com/{verApi}/v10/guilds/{guildId}/bans", headers=headers)
    if gid.status_code == 403:
        messagebox.showerror(UB_TITLE, "Missing Permissions.")
        return
    elif gid.status_code != 200:
        messagebox.showerror(UB_TITLE, "Bot must be on the server")
        return
    else:
        banList = gid.json()
        if len(banList) < 1:
            messagebox.showwarning(UB_TITLE, "There is no one to unban")
            return

        ubAsk = messagebox.askyesno(UB_TITLE, f"Do you wanna unban {len(banList)} users?")
        if not ubAsk:
            return
        else:
            msg = tk.Toplevel(root)
            msg.title(UB_TITLE)
            center_window(msg, 245, 70)

            tk.Message(msg, text=f"Unbanning {len(banList)} users, please be patient!", padx=20, pady=20, width=225, font=(defFont, 10)).pack()

            if not os.path.exists("botKey.txt"):
                with open("botKey.txt", "w") as file:
                    file.write(auth)

            for unban in banList:
                userId = unban["user"]["id"]
                requests.delete(f"https://discord.com/api/{verApi}/guilds/{guildId}/bans/{userId}", headers=headers)
                time.sleep(.3)

            msg.destroy()
            messagebox.showinfo(UB_TITLE, f"Unbanned {len(banList)} users")
            return

# Tworzenie głównego okna aplikacji
def guiUnbanAll(root):
    global Authorization, enterGuildId, labels

    root.title(UB_TITLE)

    labels = []
    containerFrame = tk.Frame(root)
    labels.append(containerFrame)

    tk.Label(containerFrame, text="Authorization").pack(pady=(30,0))
    tk.Button(containerFrame, text="Where Can I Find Bot Token?", command=lambda: webbrowser.open("https://youtu.be/54d0mquJqAc"), relief="flat", bg=containerFrame.cget("bg"), fg="blue", font=(defFont, 8, "underline"), bd=0).pack()
    Authorization = tk.Entry(containerFrame)
    Authorization.pack(pady=(3,0), ipady=1)

    if os.path.exists("botKey.txt"):
        with open("botKey.txt", "r") as file:
            botKey = file.read()
            Authorization.insert(0, botKey)

    tk.Label(containerFrame, text="GuildID").pack(pady=(10,0))
    enterGuildId = tk.Entry(containerFrame)
    enterGuildId.pack(ipady=1)

    tk.Button(containerFrame, text="Unban", command=getUsers, font=(defFont, 12, "bold")).pack(pady=(20,0))

    containerFrame.pack()

def hideUnbanAll():
    for label in labels:
        label.pack_forget()
