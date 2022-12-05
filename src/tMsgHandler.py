from tMsgText import tMsgText

class tMsgHandler:
    def __init__(self, token, tMsgSender, config):
        self.token = token
        self.tMsgSender = tMsgSender
        self.config = config

    def handleMessage(self, message):
        if 'text' in message['message']:
            tMsgText(message['message'], self.tMsgSender, self.config)
