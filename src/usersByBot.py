import tkinter as tk
from tkinter import messagebox

import webbrowser, requests, time, os

from config import WINDOW_TITLE, defFont, center_window, root

def checkAuth():
    global headers, guildId, channelId, filename, cMsg, imgAmount

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
        return
    
    imgAmount = int(enterImgAmount.get() or 0)
    if boxImage.get() == 1 and imgAmount <= 0:
        messagebox.showwarning(WINDOW_TITLE, 'Enter Amount of Images')
        return
    
    cMsg = enterMessage.get()
    if boxText.get() == 1 and not cMsg:
        messagebox.showwarning(WINDOW_TITLE, 'Enter Message')
        return

    if '.txt' not in filename:
        filename += '.txt'

    if not os.path.exists("botKey.txt"):
        with open("botKey.txt", "w") as file:
            file.write(auth)

    return True

def getUsers():
    msgid = ''
    startTime = time.time()
    users = set()

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
                for userId in users:
                    userOnServer = requests.get(f'https://discord.com/api/v10/guilds/{guildId}/members/{userId}', headers=headers)
                    if userOnServer.status_code == 200:
                        user = userOnServer.json()
                        file.write(user['user']['username'] + '\n')

                genMsg.destroy()
                messagebox.showinfo(WINDOW_TITLE, f'{filename} was generated in {time.time() - startTime:.0f}s')
                return

            for message in messages:
                if boxImage.get() == 1 and boxText.get() == 1:
                    if len(message['attachments']) >= imgAmount and cMsg in message['content']:
                        users.add(message['author']['id'])
                elif boxImage.get() == 1:
                    if len(message['attachments']) >= imgAmount:
                        users.add(message['author']['id'])
                elif boxText.get() == 1:
                    if cMsg.lower() in message['content'].lower():
                        users.add(message['author']['id'])
                else:
                    users.add(message['author']['id'])

                msgid = '&before=' + message['id']
                
            time.sleep(.3)

def genStart():
    if checkAuth():
        global genMsg
        
        genMsg = tk.Toplevel(root)
        genMsg.title(WINDOW_TITLE)
        center_window(genMsg, 245, 70)

        tk.Message(genMsg, text="Don't close the app until it finishes collecting users", padx=20, pady=20, width=225, font=(defFont, 10)).pack()

        root.after(100, getUsers)

# Tworzenie głównego okna aplikacji
def guiUsers(root):
    global Authorization, enterGuildId, enterChannelId, enterFilename, entryImgAmount, enterImgAmount, entryMsg, enterMessage, boxImage, boxText, labels

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

    boxImage = tk.IntVar()
    tk.Checkbutton(containerFrame, text="Check Images", variable=boxImage, command=vImage, font=(defFont, 10)).pack(pady=(10,0))

    entryImgAmount = tk.Frame(containerFrame)
    entryImgAmount.pack()
    enterImgAmount = tk.Entry(entryImgAmount, textvariable=tk.StringVar(value="1"))

    boxText = tk.IntVar()
    tk.Checkbutton(containerFrame, text="Check Message", variable=boxText, command=vMessage, font=(defFont, 10)).pack()

    entryMsg = tk.Frame(containerFrame)
    entryMsg.pack()
    enterMessage = tk.Entry(entryMsg)

    tk.Button(containerFrame, text="Generate", command=genStart, font=(defFont, 12, "bold")).pack(pady=(15,0))

    containerFrame.pack()

def vMessage():
    if boxText.get() == 1:
        enterMessage.pack(ipady=1)
    else:
        entryMsg.configure(height=1)
        enterMessage.pack_forget()

def vImage():
    if boxImage.get() == 1:
        enterImgAmount.pack(ipady=1)
    else:
        entryImgAmount.configure(height=1)
        enterImgAmount.pack_forget()

def hideUsersFile():
    for label in labels:
        label.pack_forget()