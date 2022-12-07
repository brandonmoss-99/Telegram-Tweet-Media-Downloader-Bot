import requests

class tMsgSender:
    def __init__(self, token):
        self.token = token

    def generateRequest(self, msgParams):
        # if there's multiple parameters, have to append them correctly
        if len(msgParams) > 3:
            requestString = f"https://api.telegram.org/bot{str(self.token)}/{str(msgParams[0])}?"
            # skip the 0th item, already appended it to the requestString
            for i in range(1, len(msgParams)-3, 2):
                f"{requestString}{str(msgParams[i])}={str(msgParams[i+1])}&"
                requestString = f"{requestString}{str(msgParams[i])}={str(msgParams[i+1])}&"
            requestString = f"{requestString}{str(msgParams[-2])}={str(msgParams[-1])}"
        elif len(msgParams) > 1:
            requestString = f"https://api.telegram.org/bot{str(self.token)}/{str(msgParams[0])}?{str(msgParams[1])}={str(msgParams[2])}"
        else:
            requestString = f"https://api.telegram.org/bot{str(self.token)}/{str(msgParams[0])}"
        return requestString

    def sendRequest(self, msgParams):
        requestString = self.generateRequest(msgParams)

        try:
            request = requests.get(requestString)
            # return True/False for a status code of 2XX, the status code itself and the response content
            if request.ok:
                return [True, request.status_code, request.content]
            else:
                return [False, request.status_code, request.content]
        except Exception as e:
            return [False, 0, "Error whilst making the request:", requestString, "\nError:",str(e)]
