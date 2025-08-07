import tkinter as tk
from tkinter import messagebox

import webbrowser, requests, time, os

from config import WINDOW_TITLE, defFont, center_window, root

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
    
    filename = enterFilename.get()
    if not filename:
        messagebox.showwarning(WINDOW_TITLE, 'Enter Filename')
        return
    
    cMsg = enterMessage.get()
    if boxText.get() == 1 and not cMsg:
        messagebox.showwarning(WINDOW_TITLE, 'Enter Message')
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

            if not messages:
                if len(users) < 1:
                    genMsg.destroy()
                    file.close()
                    os.remove(filename)

                    messagebox.showinfo(WINDOW_TITLE, f'No users found')
                    return
                ######
                file.writelines(user + '\n' for user in users)
                genMsg.destroy()
                
                messagebox.showinfo(WINDOW_TITLE, f'{filename} was generated with {len(users)} users in {time.time() - startTime:.0f}s')
                return

            for message in messages:
                if boxImage.get() == 1 and boxText.get() == 1:
                    if len(message['attachments']) > 0 and cMsg in message['content']:
                        users.add(message['author']['username'])
                elif boxImage.get() == 1:
                    if len(message['attachments']) > 0:
                        users.add(message['author']['username'])
                elif boxText.get() == 1:
                    if cMsg.lower() in message['content'].lower():
                        users.add(message['author']['username'])
                else:
                    users.add(message['author']['username'])

                msgid = '&before=' + message['id']
                
def genStart():
    global genMsg
    
    genMsg = tk.Toplevel(root)
    genMsg.title(WINDOW_TITLE)
    center_window(genMsg, 245, 70)

    tk.Message(genMsg, text="Don't close the app until it finishes collecting users", padx=20, pady=20, width=225, font=(defFont, 10)).pack()

    root.after(100, getUsers)

# Tworzenie głównego okna aplikacji
def guiUsersClassic(root):
    global Authorization, enterChannelId, enterFilename, enterMessage, boxImage, boxText, btn, labels

    labels = []
    containerFrame = tk.Frame(root)
    labels.append(containerFrame)

    tk.Label(containerFrame, text="Authorization Key").pack(pady=(30,0))
    tk.Button(containerFrame, text="Where Can I Find Authorization Key?", command=lambda: webbrowser.open("https://www.youtube.com/watch?v=LnBnm_tZlyU"), relief="flat", bg=containerFrame.cget("bg"), fg="blue", font=(defFont, 8, "underline"), bd=0).pack()
    Authorization = tk.Entry(containerFrame)
    Authorization.pack(pady=(3,0), ipady=1)

    if os.path.exists("authKey.txt"):
        with open("authKey.txt", "r") as file:
            authKey = file.read()
            Authorization.insert(0, authKey)

    tk.Label(containerFrame, text="ChannelID").pack(pady=(10,0))
    enterChannelId = tk.Entry(containerFrame)
    enterChannelId.pack(ipady=1)

    tk.Label(containerFrame, text="Filename").pack(pady=(10,0))
    enterFilename = tk.Entry(containerFrame)
    enterFilename.pack(ipady=1)

    boxImage = tk.IntVar(value=1)
    tk.Checkbutton(containerFrame, text="Only With Images", variable=boxImage, font=(defFont, 10)).pack(pady=(10,0))

    boxText = tk.IntVar()
    tk.Checkbutton(containerFrame, text="Check Message", variable=boxText, command=vMessage, font=(defFont, 10)).pack()

    entryMsg = tk.Frame(containerFrame)
    entryMsg.pack()
    enterMessage = tk.Entry(entryMsg)
    
    btn = tk.Button(containerFrame, text="Generate", command=genStart, font=(defFont, 12, "bold"))
    btn.pack(pady=(20,0))

    containerFrame.pack()

def vMessage():
    if boxText.get() == 1:
        btn.pack_configure(pady=(20,0))
        enterMessage.pack(ipady=1)
    else:
        btn.pack_configure(pady=0)
        enterMessage.pack_forget()

def hideUsersFileClassic():
    for label in labels:
        label.pack_forget()