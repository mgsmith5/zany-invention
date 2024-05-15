import requests
import json
import os
import maskpass
from time import sleep
import sys

CMD = ""

if sys.platform == "nt":
    CMD = "cls"
else:
    CMD = "clear"


reading = True
os.system(CMD)
oldMessages = [""]
serverId = ""
channelId = ""
lastMessageId = ""
lastChannelId = ""
selectedGuild = 0
selectedChannel = 0

print("Login to discord:")
login = input("Please enter your Username: ")
password = maskpass.askpass("Please enter your Password: ")

loginPayload = {
    "login": login,
    "password": password
}
loginHeader = {
    "Content-Type": 'application/json'
}

log = requests.post("https://discord.com/api/v9/auth/login", json=loginPayload, headers=loginHeader)
log = json.dumps(log.json())
log = json.loads(log)

print(log)

Headers = {
    "Authorization": log["token"]
}




url = ""
guildsURL = "https://discord.com/api/v9/users/@me/guilds"
running = True
guilds = requests.get(guildsURL, headers=Headers)
guildsJSONDump = json.dumps(guilds.json())
guildsJSON = json.loads(guildsJSONDump)

def isSelected(id=0, currentReadGuild=0):
    if id == currentReadGuild:
        return "[x]"
    else:
        return "[]"

def formatChannels(guildID):
    global channelId
    channels = requests.get("https://discord.com/api/v9/guilds/" + guildID + "/channels", headers=Headers)
    channelsJSONDump = json.dumps(channels.json())
    channelsJSON = json.loads(channelsJSONDump)
    for i in range(len(channelsJSON)):
        print("\t", i, isSelected(selectedChannel, i), channelsJSON[i]["name"])
        if isSelected(selectedChannel, i) == "[x]":
            channelId = channelsJSON[i]["id"]
def formatGuilds():
    global serverId
    for i in range(len(guildsJSON)):
        print(i, isSelected(selectedGuild, i), guildsJSON[i]["name"])
        if i == selectedGuild:
            tempId = guildsJSON[i]["id"]
            serverId = tempId
    formatChannels(tempId)


def fetch_messages():
    global reading
    global oldMessages
    reading = True
    while reading:
        try:
            messages = requests.get('https://discord.com/api/v9/channels/' + channelId + "/messages?limit=100", headers=Headers)
            messages = json.dumps(messages.json())
            messages = json.loads(messages)
            f = len(messages)-1
            while f >= 0:
                oldMessages.append(messages[f]["content"])
                print(messages[f]["author"]["global_name"], ": ", messages[f]["content"])
                if f == 0:
                    pass
                f = f - 1

            sleep(1)
        except KeyboardInterrupt:
            reading = False
        os.system(CMD)
        
        


def refresh():
    os.system(CMD)
    formatGuilds()


def getActionCode():
    ac = input("Select Action Code: \n0: Select Server\n1: Select Channel\n2: Send Message in Selected Channel\n3: View messages in current channel\n4: Edit last message\n")
    return ac

while running:
    refresh()
    acc =getActionCode()
    if acc == "0":
        selectedGuild = int(input("Select a server id: "))
        channelId = 0
    elif acc == "1":
        selectedChannel = int(input("Select a channel: "))
    elif acc == "2":
        print(channelId)
        url = "https://discord.com/api/v9/channels/" + channelId + "/messages"
        msg = input("Message to send: ")
        payload = {
            "content" : msg
        }
        ef = requests.post(url, payload, headers=Headers)
        lastMessageId = json.dumps(ef.json())
        lastMessageId = json.loads(lastMessageId)
        lastChannelId = lastMessageId["channel_id"]
        lastMessageId = lastMessageId["id"]
    elif acc == "3":
        fetch_messages()
    elif acc == "4":
        edit = input("Enter edited text(Ctrl-C to cancel): ")
        pay = {
            "content": edit
        }
        b = requests.patch("https://discord.com/api/v9/channels/" + lastChannelId + "/messages/" + lastMessageId, pay, headers=Headers)
        b = json.dumps(b.json())
        b = json.loads(b)
        print(b)


    