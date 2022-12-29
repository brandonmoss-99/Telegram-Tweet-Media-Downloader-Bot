from tMsgSender import tMsgSender
import os, re, logging

class tMsgText:
    def __init__(self, message, tMsgSender, config):
        self.message = message
        self.getInfo()
        self.tMsgSender = tMsgSender
        self.config = config
        self.urlRegex: str = r'http[s]?://(?:[a-zA-Z]|[0-9]|[^?\s])+'


    def getInfo(self):
        # extract always included message data
        self.message_id = self.message['message_id']
        self.date = self.message['date']
        self.chat = self.message['chat']
        self.isfrom = self.message['from']


    def checkCanReply(self, id) -> bool:
        logging.debug(f"Checking if allowed to reply to userID: {id}")
        match id in self.config.allowedIds:
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
            self.tMsgSender.sendRequest(["sendMessage", "chat_id", self.chat['id'], "text", "Sorry, you're not on my allow list! Zzzz...", "disable_web_page_preview", True, "disable_notification", True])
            return
        
        # If text isn't in the message, the user most likely sent media with text in the caption instead
        if 'text' not in self.message and 'caption' in self.message:
            self.doDownloading(self.message['caption'])
            return
        
        match self.message['text']:
            case "/start":
                # what to say when a new person talks to the bot
                logging.info(f"Received /start message from userID {self.isfrom['id']}, replying with info text")
                self.tMsgSender.sendRequest(["sendMessage", "chat_id", self.chat['id'], "text", "Hi! Please send a URL to get started!", "disable_web_page_preview", True, "disable_notification", True])
            case msg:
                self.doDownloading(msg)
        

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
        # if succeeded in fetching data for valid station code, reply with info
        if data[0] == True:
            logging.debug(f"Sending sendMessage request to chat_id {self.chat['id']} with text 'Done for URL {data[1]}'")
            self.tMsgSender.sendRequest(["sendMessage", "chat_id", self.chat['id'], "text", f"Done for URL {data[1]}", "disable_web_page_preview", True, "disable_notification", True])
        else:
            logging.debug(f"Sending sendMessage request to chat_id {self.chat['id']} with text 'Failed! {data[1]}'")
            self.tMsgSender.sendRequest(["sendMessage", "chat_id", self.chat['id'], "text", f"Failed! {data[1]}", "disable_web_page_preview", True, "disable_notification", True])
