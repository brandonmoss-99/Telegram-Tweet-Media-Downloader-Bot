import time, sys, requests, random, json, logging
from tMsgSender import tMsgSender
from tMsgFetcher import tMsgFetcher, messageInfo
from tMsgText import tMsgText
from config import Config

def getHelp():
    # print help information, then quit
    logging.info("\nList of options:\n\n"+
        "(t)oken to use for telegram bot API [token]\n")
    sys.exit(0)

if __name__ == '__main__':
    print("Loading configuration")
    config: Config = Config()
    logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s', level=config.logLevel)
    config.loadEnvVars()

    # Telegram Polling Configuration
    msgOffset: int = 0
    pollTimeout: int = 120
    logging.info(f"Using max long polling timeout of {pollTimeout} seconds")

    try:
        logging.info("Attempting to verify Telegram API token")
        # connect to Telegram API with their getMe test method for checking API works
        testResponse: requests.Response = requests.get(f"https://api.telegram.org/bot{config.tToken}/getMe")
        # set the token to be used if we get a 2xx response code back
        if testResponse.ok:
            bottoken: str = config.tToken
            logging.info("Telegram API token OK")
        else:
            logging.error("Telegram API check failed")
            getHelp()
    except Exception as ex:
        logging.error("Telegram API token verification failed", exc_info=ex)
        getHelp()

    tMsgSender = tMsgSender(bottoken)
    tMsgFetcher = tMsgFetcher(bottoken, pollTimeout)

    logging.info("Getting Bot info from Telegram")
    botInfo = json.loads(tMsgSender.sendRequest(["getMe"]).content)['result']
    bot_id = botInfo['id']
    bot_username = botInfo['username']
    logging.info(f"Got bot info - ID: {bot_id}, username: {bot_username}")

    while True:
        # fetch all the new messages from Telegram servers
        logging.info("Sending off to wait for new data")
        response: messageInfo = tMsgFetcher.fetchMessages(msgOffset)
        logging.info("Received new Telegram data")
        if response.tResponseOk:
            logging.info("Telegram response was OK")
            for msg in response.tResult:
                logging.info("Handling message(s)")
                tMsgText(msg['message'], tMsgSender, config).process()
                msgOffset = msg['update_id'] + 1  # Update msg offset
                logging.info(f"Message offset updated to {msgOffset}")
        else:
            logging.warn(f"Telegram response indicated error! {response.errCode} - {response.errDesc}")
            # failed to fetch new messages, wait for random number of seconds then try again
            # (may reduce strain on telegram servers when requests are randomly distributed if
            # they go down, instead of happening at fixed rate along with many other bots etc)
            sleepTime: int = random.randint(pollTimeout, pollTimeout*2)
            logging.info(f"Sleeping for {sleepTime} seconds")
            time.sleep(sleepTime)
