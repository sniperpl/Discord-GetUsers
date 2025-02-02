import tkinter as tk
from tkinter import messagebox
import webbrowser
import requests
import json
import time
import os

def getUsers():
    auth = Authorization.get()
    if not auth:
        messagebox.showwarning("Authorization", 'Enter Bot Token')
        return
    
    headers = {
        'Authorization': f'Bot {auth}'
    }

    guildId = enterGuildId.get()
    if not guildId:
        messagebox.showwarning("Get Users", 'Enter guildId')
        return
    
    gid = requests.get(f'https://discord.com/api/v10/guilds/{guildId}', headers=headers)
    if gid.status_code == 403:
        messagebox.showerror("Get Users", "Missing Permissions.")
        return
    elif gid.status_code != 200:
        messagebox.showerror("Get Users", "Bot must be on the server")
        return

    channelId = enterChannelId.get()
    if not channelId:
        messagebox.showwarning("Get Users", 'Enter channelId')
        return
    
    cid = requests.get(f'https://discord.com/api/v10/channels/{channelId}', headers=headers)
    if cid.status_code != 200:
        messagebox.showerror("Get Users", "This channelId doesn't exist")
        return
    
    filename = enterFilename.get()
    if not filename:
        messagebox.showwarning("Get Users", 'Enter filename')
        return

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
            messages = json.loads(r.text)

            if not messages:
                for userId in users:
                    userOnServer = requests.get(f'https://discord.com/api/v10/guilds/{guildId}/members/{userId}', headers=headers)
                    if userOnServer.status_code == 200:
                        user = json.loads(userOnServer.text)
                        file.write(user['user']['username'] + '\n')

                messagebox.showinfo("Get Users", f'{filename} was generated in {time.time() - startTime:.0f}s')
                return

            for message in messages:
                users.add(message['author']['id'])
                msgid = '&before=' + message['id']
                
            time.sleep(.5)

# Tworzenie głównego okna aplikacji
def guiUsers(root):
    global Authorization, enterGuildId, enterChannelId, enterFilename, labels

    root.title("Get Users by bot")

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

    label_channelId = tk.Label(Frame, text="channelId")
    label_channelId.pack(pady=(6,0))
    enterChannelId = tk.Entry(Frame)
    enterChannelId.pack()

    label_filename = tk.Label(Frame, text="filename")
    label_filename.pack(pady=(6,0))
    enterFilename = tk.Entry(Frame)
    enterFilename.pack()

    submitButton = tk.Button(Frame, text="Generate", command=getUsers)
    submitButton.pack(pady=(20,0))

    Frame.pack()

def hideUsersFile():
    for label in labels:
        label.pack_forget()