import time, sys, requests, random, json
from tMsgSender import tMsgSender
from tMsgFetcher import tMsgFetcher
from tMsgHandler import tMsgHandler
from config import Config

def getHelp():
    # print help information, then quit
    print("\nList of options:\n\n"+
        "(t)oken to use for telegram bot API [token]\n")
    sys.exit(0)

if __name__ == '__main__':
    # Telegram Polling Configuration
    msgOffset = 0
    pollTimeout = 60

    config = Config()
    config.loadEnvVars()

    try:
        # connect to Telegram API with their getMe test method for checking API works
        testResponse = requests.get("https://api.telegram.org/bot%s/getMe" % (config.tToken))
        # set the token to be used if we get a 2xx response code back
        if testResponse.ok:
            bottoken = config.tToken
        else:
            print("Error validating your token!")
            getHelp()
    except Exception as ex:
        print("Error trying to validate your token!", ex)
        getHelp()
    
    print("--------------------------------------\nProgram started at UNIX time:", int(time.time()), "\n")

    tMsgSender = tMsgSender(bottoken)
    tMsgFetcher = tMsgFetcher(bottoken, pollTimeout)
    tMsgHandler = tMsgHandler(bottoken, tMsgSender, config)

    botInfo = json.loads(tMsgSender.sendRequest(["getMe"])[2])['result']
    bot_id = botInfo['id']
    bot_username = botInfo['username']

    while True:
        # fetch all the new messages from Telegram servers
        if tMsgFetcher.fetchMessages(msgOffset):
            # for each message in the list of new messages
            for i in range(tMsgFetcher.getMessagesLength()):
                # get the message
                msg = tMsgFetcher.getMessage(i)
                if 'message' in msg:
                    # check the message type and hand message off to handler
                    tMsgHandler.handleMessage(msg)
                
                # update the message offset, so it is 'forgotten' by telegram servers
                # and not returned again on next fetch for new messages, as we've
                # (hopefully) dealt with the message now
                msgOffset = msg['update_id'] + 1
        else:
                # failed to fetch new messages, wait for random number of seconds then try again
                # (may reduce strain on telegram servers when requests are randomly distributed if
                # they go down, instead of happening at fixed rate along with many other bots etc)
                time.sleep(random.randint(pollTimeout, pollTimeout*2))

