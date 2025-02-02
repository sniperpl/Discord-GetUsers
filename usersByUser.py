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
        messagebox.showwarning("Get Users", 'Enter Authorization Key')
        return
    
    headers = {
        'Authorization': auth
    }

    authkey = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
    if authkey.status_code != 200:
        messagebox.showerror("Get Users", "Wrong Authorization Key")
        return

    channelId = enterChannelId.get()
    if not channelId:
        messagebox.showwarning("Get Users", 'Enter ChannelID')
        return
    
    r = requests.get(f'https://discord.com/api/v10/channels/{channelId}', headers=headers)
    if r.status_code != 200:
        messagebox.showerror("Get Users", "This ChannelID doesn't exist")
        return
    
    filename = enterFilename.get()
    if not filename:
        messagebox.showwarning("Get Users", 'Enter Filename')
        return

    if '.txt' not in filename:
        filename += '.txt'

    msgid = ''
    startTime = time.time()
    users = set()

    if not os.path.exists("authKey.txt"):
        with open("authKey.txt", "w") as file:
            file.write(auth)

    with open(filename, 'w', encoding='utf-8') as file:
        while True:
            r = requests.get(f'https://discord.com/api/v10/channels/{channelId}/messages?limit=100{msgid}', headers=headers)
            messages = json.loads(r.text)

            if not messages:
                messagebox.showinfo("Get Users", f'{filename} was generated with {len(users)} users in {time.time() - startTime:.0f}s')
                break

            for message in messages:
                users.add(message['author']['username'])
                msgid = '&before=' + message['id']
            
        file.writelines(user + '\n' for user in users)

# Tworzenie głównego okna aplikacji
def guiUsersClassic(root):
    global Authorization, enterChannelId, enterFilename, labels

    root.title("Get Users by you")

    labels = []
    Frame = tk.Frame(root)
    labels.append(Frame)

    label_Authorization = tk.Label(Frame, text="Authorization Key:")
    label_Authorization.pack(pady=(30,0))
    button_Authorization = tk.Button(Frame, text="Where Can I Find Authorization Key?", command=lambda: webbrowser.open("https://www.youtube.com/watch?v=LnBnm_tZlyU"), relief="flat", bg=Frame.cget("bg"), fg="blue", font=("Arial", 8, "underline"), bd=0)
    button_Authorization.pack()
    Authorization = tk.Entry(Frame)
    Authorization.pack(pady=(1,0))

    if os.path.exists("authKey.txt"):
        with open("authKey.txt", "r") as file:
            authKey = file.read()
            Authorization.insert(0, authKey)

    label_channelId = tk.Label(Frame, text="ChannelID:")
    label_channelId.pack(pady=(6,0))
    enterChannelId = tk.Entry(Frame)
    enterChannelId.pack()

    label_filename = tk.Label(Frame, text="Filename:")
    label_filename.pack(pady=(6,0))
    enterFilename = tk.Entry(Frame)
    enterFilename.pack()

    submitButton = tk.Button(Frame, text="Generate", command=getUsers)
    submitButton.pack(pady=(20,0))

    Frame.pack()

def hideUsersFileClassic():
    for label in labels:
        label.pack_forget()