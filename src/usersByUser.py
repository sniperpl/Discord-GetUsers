import tkinter as tk
from tkinter import messagebox

import webbrowser, requests, time, os

from config import root, verApi, defFont, WINDOW_TITLE, center_window

def checkAuth():
    global headers, channelId, filename, cMsg, imgAmount

    auth = Authorization.get()
    if not auth:
        messagebox.showwarning(WINDOW_TITLE, "Enter Authorization Key")
        return
    
    headers = {
        "Authorization": auth
    }

    authkey = requests.get(f"https://discord.com/api/{verApi}/users/@me", headers=headers)
    if authkey.status_code in (500, 502):
        messagebox.showwarning(WINDOW_TITLE, "Problem with Discord API")
        return
    elif authkey.status_code != 200:
        messagebox.showerror(WINDOW_TITLE, "Wrong Authorization Key")
        return

    channelId = enterChannelId.get()
    if not channelId:
        messagebox.showwarning(WINDOW_TITLE, "Enter ChannelID")
        return
    
    cid = requests.get(f"https://discord.com/api/{verApi}/channels/{channelId}", headers=headers)
    if cid.status_code != 200:
        messagebox.showerror(WINDOW_TITLE, "This ChannelID doesn't exist")
        return
    
    filename = enterFilename.get()
    if not filename:
        messagebox.showwarning(WINDOW_TITLE, "Enter Filename")
        return
    
    imgAmount = int(enterImgAmount.get() or 0)
    if boxImage.get() == 1 and imgAmount <= 0:
        messagebox.showwarning(WINDOW_TITLE, "Enter Amount of Images")
        return
    
    cMsg = enterMessage.get()
    if boxText.get() == 1 and not cMsg:
        messagebox.showwarning(WINDOW_TITLE, "Enter Message")
        return

    if ".txt" not in filename:
        filename += ".txt"

    if not os.path.exists("authKey.txt"):
        with open("authKey.txt", "w") as file:
            file.write(auth)

    return True

def getUsers():
    msgid = ""
    startTime = time.time()
    users = set()

    with open(filename, "w", encoding="utf-8") as file:
        while True:
            r = requests.get(f"https://discord.com/api/{verApi}/channels/{channelId}/messages?limit=100{msgid}", headers=headers)
            messages = r.json()

            if not messages:
                if len(users) < 1:
                    genMsg.destroy()
                    file.close()
                    os.remove(filename)

                    messagebox.showinfo(WINDOW_TITLE, f"No users found")
                    return
                ######
                file.writelines(user + "\n" for user in users)
                genMsg.destroy()
                
                messagebox.showinfo(WINDOW_TITLE, f"{filename} was generated with {len(users)} users in {time.time() - startTime:.0f}s")
                return

            for message in messages:
                if boxImage.get() == 1 and boxText.get() == 1:
                    if len(message["attachments"]) >= imgAmount and cMsg.lower().strip() in message["content"].lower():
                        users.add(message["author"]["username"])
                elif boxImage.get() == 1:
                    if len(message["attachments"]) >= imgAmount:
                        users.add(message["author"]["username"])
                elif boxText.get() == 1:
                    if cMsg.lower().strip() in message["content"].lower():
                        users.add(message["author"]["username"])
                else:
                    users.add(message["author"]["username"])

                msgid = "&before=" + message["id"]
                
def genStart():
    if checkAuth():
        global genMsg
        
        genMsg = tk.Toplevel(root)
        genMsg.title(WINDOW_TITLE)
        center_window(genMsg, 245, 70)

        tk.Message(genMsg, text="Don't close the app until it finishes collecting users", padx=20, pady=20, width=225, font=(defFont, 10)).pack()

        root.after(100, getUsers)

# Tworzenie głównego okna aplikacji
def guiUsersClassic(root):
    global Authorization, enterChannelId, enterFilename, entryImgAmount, enterImgAmount, entryMessage, enterMessage, boxImage, boxText, labels

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

    boxImage = tk.IntVar()
    tk.Checkbutton(containerFrame, text="Check Images", variable=boxImage, command=vImage, font=(defFont, 10)).pack(pady=(10,0))

    entryImgAmount = tk.Frame(containerFrame)
    entryImgAmount.pack()
    enterImgAmount = tk.Entry(entryImgAmount, textvariable=tk.StringVar(value="1"))

    boxText = tk.IntVar()
    tk.Checkbutton(containerFrame, text="Check Message", variable=boxText, command=vMessage, font=(defFont, 10)).pack()

    entryMessage = tk.Frame(containerFrame)
    entryMessage.pack()
    enterMessage = tk.Entry(entryMessage)
    
    tk.Button(containerFrame, text="Generate", command=genStart, font=(defFont, 12, "bold")).pack(pady=(15,0))

    containerFrame.pack()

def vMessage():
    if boxText.get() == 1:
        enterMessage.pack(ipady=1)
    else:
        entryMessage.configure(height=1)
        enterMessage.pack_forget()

def vImage():
    if boxImage.get() == 1:
        enterImgAmount.pack(ipady=1)
    else:
        entryImgAmount.configure(height=1)
        enterImgAmount.pack_forget()

def hideUsersFileClassic():
    for label in labels:
        label.pack_forget()