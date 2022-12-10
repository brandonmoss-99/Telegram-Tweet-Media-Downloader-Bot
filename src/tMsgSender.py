import requests, logging

class tMsgSender:
    def __init__(self, token: str):
        self.token = token

    def generateRequest(self, msgParams: list):
        logging.debug("Generating request string")

        # if there's multiple parameters, have to append them correctly
        if len(msgParams) > 3:
            requestString = "https://api.telegram.org/bot"+str(self.token)+"/"+str(msgParams[0])+"?"
            # skip the 0th item, already appended it to the requestString
            for i in range(1, len(msgParams)-3, 2):
                requestString = requestString + str(msgParams[i]) + "=" + str(msgParams[i+1]) + "&"
            requestString = requestString + str(msgParams[-2]) + "=" + str(msgParams[-1])
        elif len(msgParams) > 1:
            requestString = "https://api.telegram.org/bot"+str(self.token)+"/"+str(msgParams[0])+"?"\
                +str(msgParams[1])+ "=" + str(msgParams[2])
        else:
            requestString = f"https://api.telegram.org/bot{str(self.token)}/{str(msgParams[0])}"
        logging.debug(f"Generated request string: {requestString}")
        return requestString

    def sendRequest(self, msgParams: list):
        requestString = self.generateRequest(msgParams)

        try:
            request: requests.Response = requests.get(requestString)
            # return True/False for a status code of 2XX, the status code itself and the response content
            return recievedData(request.ok, statusCode=request.status_code, content=request.content)
        except Exception as e:
            return recievedData(isOk=False, isErr=True, errDetails=f"Error making request {requestString}, {str(e)}" )

class recievedData:
    def __init__(self, isOk: bool, isErr: bool=False, statusCode: int=-1, content: bytes=bytearray(0), errDetails: str=""):
        self.ok: bool = isOk
        self.isErr: bool = isErr
        self.statusCode: int = statusCode
        self.content: bytes = content
        self.errDetails: str = errDetails
