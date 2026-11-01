import tkinter as tk
from tkinter import messagebox

import webbrowser, requests, time, os

from config import root, verApi, defFont, WINDOW_TITLE, center_window

def checkAuth():
    global headers, channelId, filename, msgid, emote

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

    msgid = enterMsgid.get()
    if not msgid:
        messagebox.showwarning(WINDOW_TITLE, "Enter Message ID")
        return
    
    emote = enterEmoji.get()
    if not emote:
        messagebox.showwarning(WINDOW_TITLE, "Enter Emoji")
        return

    cEmote = requests.get(f"https://discord.com/api/{verApi}/channels/{channelId}/messages/{msgid}/reactions/{emote}", headers=headers)
    if cEmote.status_code != 200 or (cEmote.status_code == 200 and cEmote.json() == []):
        messagebox.showerror(WINDOW_TITLE, "This Emoji doesn't exist on this MessageID")
        return

    filename = enterFilename.get()
    if not filename:
        messagebox.showwarning(WINDOW_TITLE, "Enter Filename")
        return

    if ".txt" not in filename:
        filename += ".txt"

    if not os.path.exists("authKey.txt"):
        with open("authKey.txt", "w") as file:
            file.write(auth)

    if os.path.exists("authKey.txt"):
        with open("authKey.txt", "r") as file:
            authKey = file.read()
            if authKey != auth:
                with open("authKey.txt", "w") as file:
                    file.write(auth)

    return True

def getUsers():
    startTime = time.time()
    users = 0
    after = ""

    with open(filename, "w", encoding="utf-8") as file:
        while True:
            r = requests.get(f"https://discord.com/api/{verApi}/channels/{channelId}/messages/{msgid}/reactions/{emote}?limit=100{after}", headers=headers)
            listOfUsers = r.json()

            if not listOfUsers:
                genMsg.destroy()
                messagebox.showinfo(WINDOW_TITLE, f"{filename} was generated with {users} users in {time.time() - startTime:.0f}s")
                return

            for user in listOfUsers:
                users += 1
                file.write(user['username'] + '\n')
                    
                after = "&after=" + user["id"]

def genStart():
    if checkAuth():
        global genMsg
        
        genMsg = tk.Toplevel(root)
        genMsg.title(WINDOW_TITLE)
        center_window(genMsg, 245, 70)

        tk.Message(genMsg, text="Don't close the app until it finishes collecting users", padx=20, pady=20, width=225, font=(defFont, 10)).pack()

        root.after(100, getUsers)

# Tworzenie głównego okna aplikacji
def guiUsersReactions(root):
    global Authorization, enterChannelId, enterFilename, enterMsgid, enterEmoji, labels

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

    tk.Label(containerFrame, text="Message ID").pack(pady=(10,0))
    enterMsgid = tk.Entry(containerFrame)
    enterMsgid.pack(ipady=1)

    tk.Label(containerFrame, text="Emoji").pack(pady=(10,0))
    enterEmoji = tk.Entry(containerFrame)
    enterEmoji.pack(ipady=1)

    tk.Label(containerFrame, text="Filename").pack(pady=(10,0))
    enterFilename = tk.Entry(containerFrame)
    enterFilename.pack(ipady=1)
    
    tk.Button(containerFrame, text="Generate", command=genStart, font=(defFont, 12, "bold")).pack(pady=(15,0))

    containerFrame.pack()

def hideUsersFileReactions():
    for label in labels:
        label.pack_forget()