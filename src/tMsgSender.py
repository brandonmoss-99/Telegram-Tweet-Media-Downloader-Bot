import requests, logging

class recievedData:
    def __init__(self, isOk: bool, isErr: bool=False, statusCode: int=-1, content: bytes=bytearray(0), errDetails: str=""):
        self.ok: bool = isOk
        self.isErr: bool = isErr
        self.statusCode: int = statusCode
        self.content: bytes = content
        self.errDetails: str = errDetails

class tMsgSender:
    def __init__(self, token: str):
        self.token = token
        self.tAPIUrl: str = f"https://api.telegram.org/bot{self.token}"

    def generateRequest(self, msgParams: list) -> str:
        logging.debug("Generating request string")

        match msgParams:
            # if there's multiple parameters, have to append them correctly
            case p if len(msgParams) > 3:
                requestString = f"{self.tAPIUrl}/{str(p[0])}?"
                # skip the 0th item, already appended it to the requestString
                for i in range(1, len(p)-3, 2):
                    requestString = f"{requestString}{str(p[i])}={str(p[i+1])}&"
                requestString = f"{requestString}{str(p[-2])}={str(p[-1])}"
            case p if len(msgParams) > 1:
                requestString = f"{self.tAPIUrl}/{str(p[0])}?{str(p[1])}={str(p[2])}"
            case p:
                requestString = f"{self.tAPIUrl}/{str(p[0])}"
        logging.debug(f"Generated request string: {requestString}")
        return requestString

    def sendGetMe(self) -> recievedData:
        return self.sendRequest(["getMe"])
    
    def sendGetUpdates(self, msgOffset: int, pollTimeout: int, updatesToFetch: str) -> recievedData:
        return self.sendRequest(["getUpdates", "offset", msgOffset, "timeout", pollTimeout, "allowed_updates", updatesToFetch])

    def sendMessage(self, text: str, chat_id: str) -> recievedData:
        return self.sendRequest(["sendMessage", "chat_id", chat_id, "text", text, "disable_web_page_preview", True])
    
    def sendSilentMessage(self, text: str, chat_id: str) -> recievedData:
        return self.sendRequest(["sendMessage", "chat_id", chat_id, "text", text, "disable_web_page_preview", True, "disable_notification", True])

    # def sendPhoto(self, photo_path: str, chat_id: str) -> recievedData:
    #     return self.sendRequest(["sendPhoto", "chat_id", chat_id], files={"photo": open(photo_path, "rb")})

    # def sendVideo(self, video_path: str, chat_id: str) -> recievedData:
    #     return self.sendRequest(["sendVideo", "chat_id", chat_id], files={"video": open(video_path, "rb")})

    def sendMultiplePhotos(self,photo_paths: list, chat_id: str,  caption: str=None):
        """
        Send multiple photos in a single message
        
        Arguments:
        chat_id: str -- The ID of the chat where message should be sent
        photo_files: list -- List of file objects representing photos to be sent.
        caption: str or None -- Caption for the photos. If None, no caption will be sent.
        """
        url = f"{self.tAPIUrl}/sendMediaGroup"
        media = []
        files = [('photo' + str(i), open(photo_path, 'rb')) for i, photo_path in enumerate(photo_paths)]
        for photo_file in files:
            media.append({
                "type": "photo",
                "media": photo_file
            })
        
        payload = {
            "chat_id": chat_id,
            "media": media
        }
        
        if caption is not None:
            payload["caption"] = caption
        
        response = requests.post(url, json=payload)
        logging.info(response)
        if response.status_code != 200:
            raise Exception(f"Failed to send message. Status code: {response.status_code}")
    # def sendMultiplePhotos(self, photo_paths, chat_id: str) -> recievedData:
    #     files = [('photo' + str(i), open(photo_path, 'rb')) for i, photo_path in enumerate(photo_paths)]
    #     logging.info("#####################")
    #     logging.info(files)
    #     params = ['sendMediaGroup', 'chat_id', chat_id]

    #     return self.sendRequest(params, files)


    def sendRequest(self, msgParams: list, files=None) -> recievedData:
        requestString = self.generateRequest(msgParams)

        try:
            if files is None:
                response = requests.get(requestString)
            else:
                response = requests.post(requestString, files=files)
            logging.info(response)
            return recievedData(response.ok, statusCode=response.status_code, content=response.content)
        except Exception as e:
            return recievedData(isOk=False, isErr=True, errDetails=f"Error making request {requestString}, {str(e)}")
