import tkinter as tk
from tkinter import messagebox

import webbrowser, requests, time, os

from config import root, verApi, defFont, WINDOW_TITLE, center_window

def checkAuth():
    global headers, guildId, roleId, filename

    auth = Authorization.get()
    if not auth:
        messagebox.showwarning(WINDOW_TITLE, "Enter Bot Token")
        return
    
    headers = {
        "Authorization": f"Bot {auth}"
    }

    authkey = requests.get(f"https://discord.com/api/{verApi}/users/@me", headers=headers)
    if authkey.status_code in (500, 502):
        messagebox.showwarning(WINDOW_TITLE, "Problem with Discord API")
        return
    elif authkey.status_code != 200:
        messagebox.showerror(WINDOW_TITLE, "Wrong Authorization Key")
        return
    
    guildId = enterGuildId.get()
    if not guildId:
        messagebox.showwarning(WINDOW_TITLE, "Enter GuildID")
        return
    
    gid = requests.get(f"https://discord.com/api/{verApi}/guilds/{guildId}?with_counts=true", headers=headers)
    if gid.status_code == 403:
        messagebox.showerror(WINDOW_TITLE, "Missing Permissions")
        return
    elif gid.status_code != 200:
        messagebox.showerror(WINDOW_TITLE, "Bot must be on the server")
        return
    
    roleId = enterRoleId.get()
    if not roleId:
        messagebox.showwarning(WINDOW_TITLE, "Enter RoleID")
        return

    rid = requests.get(f"https://discord.com/api/{verApi}/guilds/{guildId}/roles/{roleId}", headers=headers)
    if rid.status_code == 403:
        messagebox.showerror(WINDOW_TITLE, "Missing Permissions")
        return
    elif rid.status_code != 200:
        messagebox.showerror(WINDOW_TITLE, "Unknown RoleID")
        return

    filename = enterFilename.get()
    if not filename:
        messagebox.showwarning(WINDOW_TITLE, "Enter Filename")
        return
    
    if ".txt" not in filename:
        filename += ".txt"

    if not os.path.exists("botKey.txt"):
        with open("botKey.txt", "w") as file:
            file.write(auth)

    return True

def getUsers():
    userId = ""
    startTime = time.time()
    users = 0

    with open(filename, "w", encoding="utf-8") as file:
        while True:
            r = requests.get(f"https://discord.com/api/{verApi}/guilds/{guildId}/members?limit=1000{userId}", headers=headers)
            if r.status_code == 403:
                genMsg.destroy()
                file.close()
                os.remove(filename)

                webbrowser.open("https://discord.com/developers/applications")
                messagebox.showwarning(WINDOW_TITLE, f"Set on Discord Developer Portal: Choose Bot → Bot → Privileged Gateway Intents → Server Members Intent (GUILD_MEMBERS) and Try Again")
                return

            members = r.json()

            for member in members:
                if "roles" in member and isinstance(member["roles"], list):
                    if roleId in member["roles"]:
                        file.write(member["user"]["username"] + "\n")
                        users += 1

            if len(members):
                userId = "&after=" + members[-1]["user"]["id"]
                time.sleep(.3)
            elif users == 0:
                genMsg.destroy()
                file.close()
                os.remove(filename)

                messagebox.showinfo(WINDOW_TITLE, f"No users found")
                return
            else:
                genMsg.destroy()
                messagebox.showinfo(WINDOW_TITLE, f"{filename} was generated with {users} users in {time.time() - startTime:.0f}s")
                return


def genStart():
    if checkAuth():
        global genMsg
        
        genMsg = tk.Toplevel(root)
        genMsg.title(WINDOW_TITLE)
        center_window(genMsg, 245, 70)

        tk.Message(genMsg, text="Don't close the app until it finishes collecting users", padx=20, pady=20, width=225, font=(defFont, 10)).pack()

        root.after(100, getUsers)

def guiUsersRole(root):
    global Authorization, enterGuildId, enterRoleId, enterFilename, labels

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

    tk.Label(containerFrame, text="RoleID").pack(pady=(10,0))
    enterRoleId = tk.Entry(containerFrame)
    enterRoleId.pack(ipady=1)

    tk.Label(containerFrame, text="Filename").pack(pady=(10,0))
    enterFilename = tk.Entry(containerFrame)
    enterFilename.pack(ipady=1)

    tk.Button(containerFrame, text="Generate", command=genStart, font=(defFont, 12, "bold")).pack(pady=(15,0))

    containerFrame.pack()

def hideUsersRole():
    for label in labels:
        label.pack_forget()