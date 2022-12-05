from tMsgSender import tMsgSender
import os, re

class tMsgText:
    def __init__(self, message, tMsgSender, config):
        self.message = message
        self.getInfo()
        self.tMsgSender = tMsgSender
        self.config = config

        # Check for userID who sent the msg. Only do stuff if they're allowed to send stuff
        if self.isfrom['id'] in self.config.allowedIds:
            # if message isn't "/start" from new telegram convo
            if self.message['text'] != "/start":
                urlRegex = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
                urls = re.findall(urlRegex, self.message['text'])

                if urls is None:
                    self.reply([False, "Couldn't find a valid URL to use"])
                else:
                    for url in urls:
                        # Download the contents of the URL, and send reply
                        os.system(f"gallery-dl \"{url}\"")
                        self.reply([True, url])

            else:
                # what to say when a new person talks to the bot
                self.tMsgSender.sendRequest(["sendMessage", "chat_id", self.chat['id'], "text", "Hi! Please send a URL to get started!"])

    def getInfo(self):
        # extract always included message data
        self.message_id = self.message['message_id']
        self.date = self.message['date']
        self.chat = self.message['chat']
        self.isfrom = self.message['from']

    def reply(self, data):
        # if succeeded in fetching data for valid station code, reply with info
        if data[0] == True:
            self.tMsgSender.sendRequest(["sendMessage", "chat_id", self.chat['id'], "text", f"Done for URL {data[1]}", "disable_web_page_preview", True, "disable_notification", True])
        else:
            self.tMsgSender.sendRequest(["sendMessage", "chat_id", self.chat['id'], "text", "Failed! " + data[1]])
