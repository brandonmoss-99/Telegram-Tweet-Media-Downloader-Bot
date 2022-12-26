from tMsgText import tMsgText
from tMsgSender import tMsgSender
from config import Config
import logging

class tMsgHandler:
    def __init__(self, token: str, tMsgSender: tMsgSender, config: Config):
        self.token = token
        self.tMsgSender = tMsgSender
        self.config = config

    def handleMessage(self, message):
        if 'text' in message['message']:
            logging.info("Handling message of type 'text'")
            msg = tMsgText(message['message'], self.tMsgSender, self.config)
            msg.process()
