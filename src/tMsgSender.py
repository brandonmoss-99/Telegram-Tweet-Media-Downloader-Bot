import requests
import logging
import telegram
from telegram.ext import Updater


class recievedData:
    def __init__(self, isOk: bool, isErr: bool = False, statusCode: int = -1, content: bytes = bytearray(0), errDetails: str = ""):
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

    # def sendMultipleFiles(self, file_paths, chat_id: str, chat_id2: str) -> recievedData:
    #     upload_url_photo = self.tAPIUrl + "/sendPhoto"
    #     upload_url_video = self.tAPIUrl + "/sendVideo"
    #     upload_url_document = self.tAPIUrl + "/sendDocument"
    #     upload_params = {
    #         "chat_id": chat_id2
    #     }
    #     media_group = []

    #     # 遍历本地媒体列表，根据文件类型上传文件，并获取file_id
    #     for media in file_paths:
    #         # 判断文件类型，如果是图片，使用sendPhoto方法和photo参数
    #         if media.endswith(".jpg"):
    #             upload_files = {
    #                 "photo": open(media, "rb")
    #             }
    #             response = requests.post(
    #                 upload_url_photo, data=upload_params, files=upload_files)
    #             file_id = response.json()["result"]["photo"][-1]["file_id"]
    #             media_type = "photo"
    #         # 判断文件类型，如果是视频，使用sendVideo方法和video参数
    #         elif media.endswith(".mp4"):
    #             upload_files = {
    #                 "video": open(media, "rb")
    #             }
    #             response = requests.post(
    #                 upload_url_video, data=upload_params, files=upload_files)
    #             file_id = response.json()["result"]["video"]["file_id"]
    #             media_type = "video"
    #         # 如果文件类型不是图片或视频，跳过该文件，并打印提示信息
    #         else:
    #             upload_files = {
    #                 "document": open(media, "rb")
    #             }
    #             response = requests.post(
    #                 upload_url_document, data=upload_params, files=upload_files)
    #             file_id = response.json()["result"]["document"]["file_id"]
    #             media_type = "document"

    #         # 将上传后的媒体信息添加到媒体组中，最多10个
    #         if len(media_group) < 10:
    #             media_group.append({
    #                 "type": media_type,
    #                 "media": file_id,
    #             })
    #         else:
    #             print("Media group is full. Cannot add more.")
    #             break

    #     # 定义要发送的请求的URL，使用sendMediaGroup方法
    #     request_url = self.tAPIUrl + "/sendMediaGroup"

    #     # 定义要发送的请求的参数，使用json格式
    #     request_params = {
    #         "chat_id": chat_id,
    #         "media": media_groupWW
    #     }

    #     # 发送请求，并获取响应
    #     response = requests.post(request_url, json=request_params)
    #     logging.info(response)

    def sendMultipleFiles(self, file_paths, chat_id: str, chat_id2: str) -> recievedData:
        # Create an updater object with your bot token
        updater = Updater(token=self.tAPIUrl)
        # Get the bot instance from the updater
        bot = updater.bot
        # Create an empty list to store the media group
        media_group = []

        # Loop through the local media list, upload the files according to their type, and get the file_id
        for media in file_paths:
            try:
                # Check the file type, if it is an image, use send_photo method and photo parameter
                if media.endswith(".jpg"):
                    message = bot.send_photo(
                        chat_id=chat_id2, photo=open(media, "rb"))
                    file_id = message.photo[-1].file_id
                    media_type = "photo"
                # Check the file type, if it is a video, use send_video method and video parameter
                elif media.endswith(".mp4"):
                    message = bot.send_video(
                        chat_id=chat_id2, video=open(media, "rb"))
                    file_id = message.video.file_id
                    media_type = "video"
                # Check the file type, if it is a document, use send_document method and document parameter
                else:
                    message = bot.send_document(
                        chat_id=chat_id2, document=open(media, "rb"))
                    file_id = message.document.file_id
                    media_type = "document"
            except Exception as e:
                logging.warn(e)
                continue
            # Add the uploaded media information to the media group, up to 10
            if len(media_group) < 10:
                media_group.append({
                    "type": media_type,
                    "media": file_id,
                })
            else:
                print("Media group is full. Cannot add more.")
                break

        # Use send_media_group method to send the media group to the chat id
        bot.send_media_group(chat_id=chat_id, media=media_group)

    def sendRequest(self, msgParams: list) -> recievedData:
        requestString = self.generateRequest(msgParams)

        try:
            request: requests.Response = requests.get(requestString)
            # return True/False for a status code of 2XX, the status code itself and the response content
            return recievedData(request.ok, statusCode=request.status_code, content=request.content)
        except Exception as e:
            return recievedData(isOk=False, isErr=True, errDetails=f"Error making request {requestString}, {str(e)}")
