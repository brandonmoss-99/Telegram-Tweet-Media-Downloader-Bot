from tMsgSender import tMsgSender
from config import Config
import os, re, logging

class tMsgText:
    def __init__(self, message: dict, sender: tMsgSender, conf: Config):
        self.message: dict = message
        self.getInfo()
        self.sender: tMsgSender = sender
        self.conf: Config = conf
        self.urlRegex: str = r'http[s]?://(?:[a-zA-Z]|[0-9]|[^?\s])+'


    def getInfo(self):
        # extract always included message data
        self.message_id = self.message['message_id']
        self.date = self.message['date']
        self.chat = self.message['chat']
        self.isfrom = self.message['from']


    def checkCanReply(self, id) -> bool:
        logging.debug(f"Checking if allowed to reply to userID: {id}")
        match id in self.conf.allowedIds:
            case True: 
                logging.info(f"Allowed to reply to userID: {id}")
                return True
            case _:
                logging.info(f"Not allowed to process things from userID: {id}")
                return False


    def process(self):
        # Check for userID who sent the msg. Only do stuff if they're allowed to send stuff
        if self.checkCanReply(self.isfrom['id']) == False:
            logging.info(f"Sending not on allow list message for userID: {self.isfrom['id']}")
            self.sender.sendRequest(["sendMessage", "chat_id", self.chat['id'], "text", "Sorry, you're not on my allow list! Zzzz...", "disable_web_page_preview", True, "disable_notification", True])
            return
        
        match self.message:
            case _ if 'text' in self.message and self.message['text'] == "/start":
                # what to say when a new person talks to the bot
                logging.info(f"Received /start message from userID {self.isfrom['id']}, replying with info text")
                self.sender.sendRequest(["sendMessage", "chat_id", self.chat['id'], "text", "Hi! Please send a URL to get started!", "disable_web_page_preview", True, "disable_notification", True])
            case msg if 'text' in self.message and self.message['text'] != "/start":
                logging.info(f"Received text message from userID {self.isfrom['id']}")
                self.doDownloading(msg['text'])
            case msg if 'caption' in self.message:
                logging.info(f"Received media message with caption text from userID {self.isfrom['id']}")
                self.doDownloading(msg['caption'])
            case _:
                logging.warning(f"Received incompatible message from userID {self.isfrom['id']}")
                self.sender.sendRequest(["sendMessage", "chat_id", self.chat['id'], "text", "Incompatible message!", "disable_web_page_preview", True, "disable_notification", True])
        

    def doDownloading(self, text):
        urls: list[str] = self.parseRegex(text)
        if len(urls) > 0:
            self.downloadContent(urls)
        else:
            logging.info(f"Replying couldn't find URL to userID {self.isfrom['id']}")
            self.reply([False, "Couldn't find a valid URL to use"])


    def parseRegex(self, toParse: str) -> list[str]:
        logging.debug(f"Parsing text against regex")
        urls: list[str] = re.findall(self.urlRegex, toParse)
        logging.debug(f"Found {len(urls)} matches")
        return urls
    

    def downloadContent(self, urls: list[str]):
        for url in urls:
            # Download the contents of the URL, and send reply
            logging.info(f"Attempting to gallery-dl download content from: {url}")
            dlStatus: int = os.system(f"gallery-dl \"{url}\"")
            match dlStatus:
                case 0: 
                    logging.info(f"Replying success for {url} to userID {self.isfrom['id']}")
                    self.reply([True, url])
                case _: 
                    logging.info(f"Replying failed download for {url} to userID {self.isfrom['id']}")
                    self.reply([False, f"Encountered an error whilst downloading content for {url}"])


    def reply(self, data):
        if data[0] == True:
            logging.debug(f"Sending sendMessage request to chat_id {self.chat['id']} with text 'Done for URL {data[1]}'")
            self.sender.sendRequest(["sendMessage", "chat_id", self.chat['id'], "text", f"Done for URL {data[1]}", "disable_web_page_preview", True, "disable_notification", True])
        else:
            logging.debug(f"Sending sendMessage request to chat_id {self.chat['id']} with text 'Failed! {data[1]}'")
            self.sender.sendRequest(["sendMessage", "chat_id", self.chat['id'], "text", f"Failed! {data[1]}", "disable_web_page_preview", True, "disable_notification", True])
