import tkinter as tk
from tkinter import messagebox

import webbrowser, requests, time, os

from config import WINDOW_TITLE, defFont, center_window, root

def getUsers():
    auth = Authorization.get()
    if not auth:
        messagebox.showwarning(WINDOW_TITLE, 'Enter Bot Token')
        return
    
    headers = {
        'Authorization': f'Bot {auth}'
    }

    authkey = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
    if authkey.status_code != 200:
        messagebox.showerror(WINDOW_TITLE, "Wrong Authorization Key")
        return

    guildId = enterGuildId.get()
    if not guildId:
        messagebox.showwarning(WINDOW_TITLE, 'Enter GuildID')
        return
    
    gid = requests.get(f'https://discord.com/api/v10/guilds/{guildId}', headers=headers)
    if gid.status_code == 403:
        messagebox.showerror(WINDOW_TITLE, "Missing Permissions.")
        return
    elif gid.status_code != 200:
        messagebox.showerror(WINDOW_TITLE, "Bot must be on the server")
        return

    channelId = enterChannelId.get()
    if not channelId:
        messagebox.showwarning(WINDOW_TITLE, 'Enter ChannelID')
        return
    
    cid = requests.get(f'https://discord.com/api/v10/channels/{channelId}', headers=headers)
    if cid.status_code != 200:
        messagebox.showerror(WINDOW_TITLE, "This ChannelID doesn't exist")
        return
    
    filename = enterFilename.get()
    if not filename:
        messagebox.showwarning(WINDOW_TITLE, 'Enter Filename')
        return\

    if '.txt' not in filename:
        filename += '.txt'

    msgid = ''
    startTime = time.time()
    users = set()

    if not os.path.exists("botKey.txt"):
        with open("botKey.txt", "w") as file:
            file.write(auth)
        
    with open(filename, 'w', encoding='utf-8') as file:
        while True:
            r = requests.get(f'https://discord.com/api/v10/channels/{channelId}/messages?limit=100{msgid}', headers=headers)
            messages = r.json()

            if not messages:
                for userId in users:
                    userOnServer = requests.get(f'https://discord.com/api/v10/guilds/{guildId}/members/{userId}', headers=headers)
                    if userOnServer.status_code == 200:
                        user = userOnServer.json()
                        file.write(user['user']['username'] + '\n')

                msg.destroy()
                messagebox.showinfo(WINDOW_TITLE, f'{filename} was generated in {time.time() - startTime:.0f}s')
                return

            for message in messages:
                if cBox.get() == 1:
                    if len(message['attachments']) > 0:
                        users.add(message['author']['id'])
                else:
                    users.add(message['author']['id'])

                msgid = '&before=' + message['id']
                
            time.sleep(.3)

def genStart():
    global msg
    
    msg = tk.Toplevel(root)
    msg.title(WINDOW_TITLE)
    center_window(msg, 245, 70)

    tk.Message(msg, text="Don't close the app until it finishes collecting users", padx=20, pady=20, width=225, font=(defFont, 10)).pack()

    root.after(100, getUsers)

# Tworzenie głównego okna aplikacji
def guiUsers(root):
    global Authorization, enterGuildId, enterChannelId, enterFilename, cBox, labels

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

    tk.Label(containerFrame, text="ChannelID").pack(pady=(10,0))
    enterChannelId = tk.Entry(containerFrame)
    enterChannelId.pack(ipady=1)

    tk.Label(containerFrame, text="Filename").pack(pady=(10,0))
    enterFilename = tk.Entry(containerFrame)
    enterFilename.pack(ipady=1)

    cBox = tk.IntVar(value=1)
    tk.Checkbutton(containerFrame, text="Only With Images", variable=cBox, font=(defFont, 10)).pack(pady=(10,0))

    tk.Button(containerFrame, text="Generate", command=genStart, font=(defFont, 12, "bold")).pack(pady=(20,0))

    containerFrame.pack()

def hideUsersFile():
    for label in labels:
        label.pack_forget()