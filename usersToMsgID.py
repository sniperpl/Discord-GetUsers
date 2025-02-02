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
        messagebox.showwarning("Get Users", 'Enter Bot Token')
        return
    
    headers = {
        'Authorization': f'Bot {auth}'
    }

    authkey = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
    if authkey.status_code != 200:
        messagebox.showerror("Get Users", "Wrong Authorization Key")
        return

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
    
    msgId = enterMsgId.get()
    if not msgId:
        messagebox.showwarning("Get Users", 'Enter msgId')
        return
    
    mid = requests.get(f'https://discord.com/api/v10/channels/{channelId}/messages/{msgId}', headers=headers)
    if mid.status_code != 200:
        messagebox.showerror("Get Users", "This messageId doesn't exist on this channelId")
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

            for message in messages:
                if message['id'] == f"{msgId}":
                    for userId in users:
                        userOnServer = requests.get(f'https://discord.com/api/v10/guilds/{guildId}/members/{userId}', headers=headers)
                        if userOnServer.status_code == 200:
                            user = json.loads(userOnServer.text)
                            file.write(user['user']['username'] + '\n')

                    messagebox.showinfo('Get Users', f'{filename} was generated in {time.time() - startTime:.0f}s')
                    return

                users.add(message['author']['id'])
                msgid = '&before=' + message['id']

            time.sleep(.5)

# Tworzenie głównego okna aplikacji
def guiUsersMsgID(root):
    global Authorization, enterGuildId, enterChannelId, enterMsgId, enterFilename, labels

    root.title("Get Users to msgid")

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

    label_msgId = tk.Label(Frame, text="messageId")
    label_msgId.pack(pady=(6,0))
    enterMsgId = tk.Entry(Frame)
    enterMsgId.pack()

    label_filename = tk.Label(Frame, text="filename")
    label_filename.pack(pady=(6,0))
    enterFilename = tk.Entry(Frame)
    enterFilename.pack()

    submitButton = tk.Button(Frame, text="Generate", command=getUsers)
    submitButton.pack(pady=(20,0))

    Frame.pack()

def hideUsersFileMsgID():
    for label in labels:
        label.pack_forget()