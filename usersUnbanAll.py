import tkinter as tk
from tkinter import messagebox
import webbrowser
import requests
import time
import os

def getUsers():
    auth = Authorization.get()
    if not auth:
        messagebox.showwarning("Unban All", 'Enter Bot Token')
        return
    
    headers = {
        'Authorization': f'Bot {auth}'
    }

    guildId = enterGuildId.get()
    if not guildId:
        messagebox.showwarning("Unban All", 'Enter guildId')
        return
    
    gid = requests.get(f'https://discord.com/api/v10/guilds/{guildId}/bans', headers=headers)
    if gid.status_code == 403:
        messagebox.showerror("Unban All", "Missing Permissions.")
        return
    elif gid.status_code != 200:
        messagebox.showerror("Unban All", "Bot must be on the server")
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

    messagebox.showinfo('Unban All', f'Unbanned {len(bans)} users in {time.time() - startTime:.0f}s')
    return

# Tworzenie głównego okna aplikacji
def guiUnbanAll(root):
    global Authorization, enterGuildId, labels

    root.title("Unban All")

    labels = []
    Frame = tk.Frame(root)
    labels.append(Frame)

    label_Authorization = tk.Label(Frame, text="Authorization")
    label_Authorization.pack(pady=(30,0))
    button_Authorization = tk.Button(Frame, text="Where Can I Find Bot Token?", command=lambda: webbrowser.open("https://youtu.be/54d0mquJqAc"), relief="flat", bg=Frame.cget("bg"), fg="blue", font=("Arial", 8, "underline"), bd=0)
    button_Authorization.pack()
    Authorization = tk.Entry(Frame)
    Authorization.pack(pady=(1,0))

    if os.path.exists("botKey.txt"):
        with open("botKey.txt", "r") as file:
            botKey = file.read()
            Authorization.insert(0, botKey)

    label_guildId = tk.Label(Frame, text="guildId")
    label_guildId.pack(pady=(6,0))
    enterGuildId = tk.Entry(Frame)
    enterGuildId.pack()

    submitButton = tk.Button(Frame, text="Unban", command=getUsers)
    submitButton.pack(pady=(20,0))

    Frame.pack()

def hideUnbanAll():
    for label in labels:
        label.pack_forget()
