from tkinter import *
from tkinter import messagebox

import webbrowser
import requests
import time
import os

from config import WINDOW_TITLE

def getUsers():
    auth = Authorization.get()
    if not auth:
        messagebox.showwarning(WINDOW_TITLE, 'Enter Authorization Key')
        return
    
    headers = {
        'Authorization': auth
    }

    authkey = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
    if authkey.status_code != 200:
        messagebox.showerror(WINDOW_TITLE, "Wrong Authorization Key")
        return

    channelId = enterChannelId.get()
    if not channelId:
        messagebox.showwarning(WINDOW_TITLE, 'Enter ChannelID')
        return
    
    cid = requests.get(f'https://discord.com/api/v10/channels/{channelId}', headers=headers)
    if cid.status_code != 200:
        messagebox.showerror(WINDOW_TITLE, "This ChannelID doesn't exist")
        return
    
    msgId = enterMsgId.get()
    if not msgId:
        messagebox.showwarning(WINDOW_TITLE, 'Enter MsgID')
        return
    
    filename = enterFilename.get()
    if not filename:
        messagebox.showwarning(WINDOW_TITLE, 'Enter Filename')
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
            messages = r.json()

            for message in messages:
                if cBox.get() == 1:
                    if len(message['attachments']) > 0:
                        users.add(message['author']['username'])
                else:
                    users.add(message['author']['username'])

                if message['id'] == f"{msgId}":
                    file.writelines(user + '\n' for user in users)

                    messagebox.showinfo(WINDOW_TITLE, f'{filename} was generated with {len(users)} users in {time.time() - startTime:.0f}s')
                    return

                msgid = '&before=' + message['id']

# Tworzenie głównego okna aplikacji
def guiUsersMsgID(root):
    global Authorization, enterChannelId, enterMsgId, enterFilename, cBox, labels

    labels = []
    containerFrame = Frame(root)
    labels.append(containerFrame)

    label_Authorization = Label(containerFrame, text="Authorization Key")
    label_Authorization.pack(pady=(30,0))
    button_Authorization = Button(containerFrame, text="Where Can I Find Authorization Key?", command=lambda: webbrowser.open("https://www.youtube.com/watch?v=LnBnm_tZlyU"), relief="flat", bg=containerFrame.cget("bg"), fg="blue", font=("Arial", 8, "underline"), bd=0)
    button_Authorization.pack()
    Authorization = Entry(containerFrame)
    Authorization.pack(pady=(1,0))

    if os.path.exists("authKey.txt"):
        with open("authKey.txt", "r") as file:
            botKey = file.read()
            Authorization.insert(0, botKey)

    label_channelId = Label(containerFrame, text="ChannelID")
    label_channelId.pack(pady=(10,0))
    enterChannelId = Entry(containerFrame)
    enterChannelId.pack()

    label_msgId = Label(containerFrame, text="MessageID")
    label_msgId.pack(pady=(10,0))
    enterMsgId = Entry(containerFrame)
    enterMsgId.pack()

    label_filename = Label(containerFrame, text="Filename")
    label_filename.pack(pady=(10,0))
    enterFilename = Entry(containerFrame)
    enterFilename.pack()

    cBox = IntVar(value=1)
    isOnlyImages = Checkbutton(containerFrame, text="Only With Images", variable=cBox)
    isOnlyImages.pack(pady=(10,0))

    submitButton = Button(containerFrame, text="Generate", command=getUsers)
    submitButton.pack(pady=(20,0))

    containerFrame.pack()

def hideUsersFileMsgID():
    for label in labels:
        label.pack_forget()