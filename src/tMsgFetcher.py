import requests, json, time
from tMsgSender import tMsgSender

# handles fetching of messages, returning basic message info
class tMsgFetcher:
    def __init__(self, token, pollTimeout=20):
        self.token = token
        self.pollTimeout = pollTimeout
        self.messages = None
        self.messagesParsed = None

        # create MsgSender to send requests to fetch new messages, 
        # using the same token for sending as for recieving
        self.tMsgSender = tMsgSender(token)

    # get new messages, pass in offset of last message to fetch only new ones
    # and mark to telegram servers it can remove messages older than that
    def fetchMessages(self, msgOffset):
        # get updates via long polling (sends HTTPS request, won't hear anything back from API server)
        # until there is a new update to send back, may hang here for a while
        # define which updates want telegram to send us, ignore every other update type
        updatesToFetch = '["message", "callback_query"]'
        updateRequest = self.tMsgSender.sendRequest(["getUpdates", "offset", msgOffset, "timeout", self.pollTimeout, "allowed_updates", updatesToFetch])
        if updateRequest[0] == True:
            self.messagesParsed = json.loads(updateRequest[2])
            return True
        else:
            print("timestamp:", int(time.time()), "Failed to fetch new messages!", updateRequest[2])
            return False

    # loop through each parsed message stored in the messageFetcher
    def printAllMessages(self):
        for i in range(0, len(self.messagesParsed['result'])):
            print(self.messagesParsed['result'][i],'\n\n')

    def getMessagesLength(self):
        return len(self.messagesParsed['result'])

    # return all messages stored in class
    def getMessages(self):
        return self.messagesParsed

    # return specific message stored in class by position
    def getMessage(self, pos):
        return self.messagesParsed['result'][pos]

    # print specific message stored in class by position
    def printMessage(self, pos):
        print(self.messagesParsed['result'][pos])
