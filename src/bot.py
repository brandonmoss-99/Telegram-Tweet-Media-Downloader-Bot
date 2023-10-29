import time, sys, requests, random, json, logging, subprocess
from tMsgSender import tMsgSender
from tMsgFetcher import tMsgFetcher, messageInfo
from tMsgText import tMsgText
from config import Config

class bot:
    def __init__(self):
        self.msgOffset: int = 0
        self.pollTimeout: int = 50
        logging.info(f"Using max long polling timeout of {self.pollTimeout} seconds")

    def getHelp(self):
        # print help information, then quit
        logging.info("\nList of options:\n\n"+
            "(t)oken to use for telegram bot API [token]\n")
        sys.exit(0)

    def handleMessage(self, msg):
        logging.info("Handling message(s)")
        tMsgText(msg['message'], self.sender, conf).process()
        self.msgOffset = msg['update_id'] + 1  # Update msg offset
        logging.info(f"Message offset updated to {self.msgOffset}")
    
    def verifyAPIToken(self):
        try:
            logging.info("Attempting to verify Telegram API token")
            # connect to Telegram API with their getMe test method for checking API works
            testResponse: requests.Response = requests.get(f"https://api.telegram.org/bot{conf.tToken}/getMe")
            # set the token to be used if we get a 2xx response code back
            match testResponse.ok:
                case True:
                    self.bottoken: str = conf.tToken
                    logging.info("Telegram API token OK")
                case _:
                    logging.error("Telegram API check failed")
                    self.getHelp()
        except Exception as ex:
            logging.error("Telegram API token verification failed", exc_info=ex)
            self.getHelp()
    
    def createSenderFetcher(self):
        self.sender: tMsgSender = tMsgSender(self.bottoken)
        self.fetcher: tMsgFetcher = tMsgFetcher(self.bottoken, self.pollTimeout)
    
    def getBotInfo(self):
        logging.info("Getting Bot info from Telegram")
        self.botInfo = json.loads(self.sender.sendGetMe().content)['result']
        self.bot_id = self.botInfo['id']
        self.bot_username = self.botInfo['username']
        logging.info(f"Got bot info - ID: {self.bot_id}, username: {self.bot_username}")
    
    def run(self):
        self.createSenderFetcher()
        self.getBotInfo()
        while True:
            # fetch all the new messages from Telegram servers
            logging.info("Sending off to wait for new data")
            response: messageInfo = self.fetcher.fetchMessages(self.msgOffset)
            logging.info("Received new Telegram data")
            match response.tResponseOk:
                case True:
                    logging.info("Telegram response was OK")
                    list(map(lambda x: self.handleMessage(x), response.tResult))
                case _:
                    logging.warning(f"Telegram response indicated error! {response.errCode} - {response.errDesc}")
                    # failed to fetch new messages, wait for random number of seconds then try again
                    sleepTime: int = random.randint(self.pollTimeout, self.pollTimeout*2)
                    logging.info(f"Sleeping for {sleepTime} seconds")
                    time.sleep(sleepTime)


if __name__ == '__main__':
    print("Loading configuration")
    conf: Config = Config()
    logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s', level=conf.logLevel)
    conf.loadEnvVars()
    galleryDlVersion = subprocess.run(["gallery-dl", "--version"], capture_output=True)
    logging.info(f"Using gallery-dl version: {galleryDlVersion.stdout}")

    # Telegram Polling Configuration
    tBot: bot = bot()
    tBot.verifyAPIToken()
    tBot.run()