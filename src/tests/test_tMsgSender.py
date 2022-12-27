import unittest
from tMsgSender import tMsgSender

class Test_generateRequest(unittest.TestCase):
    def setUp(self) -> None:
        self.tToken = "AAAAA:123456789"
        self.tSender = tMsgSender(self.tToken)
    
    # A test for generating a URL from 1 msgParam
    def test_getMe(self) -> None:
        self.assertEqual(self.tSender.generateRequest(["getMe"]), f"https://api.telegram.org/bot{self.tToken}/getMe")

    # A test for generating a URL from 3 msgParams
    def test_getUpdates(self) -> None:
        request = ["getUpdates", "offset", 1]
        correctURL = f"https://api.telegram.org/bot{self.tToken}/getUpdates?offset=1"
        self.assertEqual(self.tSender.generateRequest(request), correctURL)

    # A test for generating a URL from many msgParams
    def test_sendMsg(self) -> None:
        request = ["sendMessage", "chat_id", 123456789, "text", "testText", "disable_web_page_preview", True, "disable_notification", True]
        correctURL = f"https://api.telegram.org/bot{self.tToken}/sendMessage?chat_id=123456789&text=testText&disable_web_page_preview=True&disable_notification=True"
        self.assertEqual(self.tSender.generateRequest(request), correctURL)
        

if __name__ == '__main__':
    unittest.main()