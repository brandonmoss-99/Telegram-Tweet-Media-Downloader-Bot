import json, logging
from tMsgSender import tMsgSender, recievedData

class messageInfo:
    def __init__(self, ok: bool, result:dict={}, errCode: int=-1, errDesc:str=""):
        self.tResponseOk: bool = ok
        self.tResult: dict = result
        self.errCode: int = errCode
        self.errDesc: str = errDesc

# handles fetching of messages, returning message info
class tMsgFetcher:
    def __init__(self, token: str, pollTimeout: int=20):
        self.token: str = token
        self.pollTimeout: int = pollTimeout
        self.updatesToFetch: str = '["message"]'

        # create MsgSender to send requests to fetch new messages, 
        # using the same token for sending as for recieving
        self.tMsgSender: tMsgSender = tMsgSender(token)

    # get new messages, pass in offset of last message to fetch only new ones
    # and mark to telegram servers it can remove messages older than that
    def fetchMessages(self, msgOffset: int):
        # get updates via long polling (sends HTTPS request, won't hear anything back from API server)
        # until there is a new update to send back, may hang here for a while
        updateResponse: recievedData = self.tMsgSender.sendRequest(["getUpdates", "offset", msgOffset, "timeout", self.pollTimeout, "allowed_updates", self.updatesToFetch])

        if updateResponse.isErr:
            logging.error(f"Failed to fetch new messages! Got HTTP {updateResponse.statusCode} - {updateResponse.errDetails}")
            return messageInfo(False, errCode=updateResponse.statusCode, errDesc=updateResponse.errDetails)

        messagesParsed = json.loads(updateResponse.content)

        match messagesParsed['ok']:
            case True: return messageInfo(True, result=messagesParsed['result'])
            case _: return messageInfo(False, errCode=messagesParsed['error_code'], errDesc=messagesParsed['description'])
