import unittest, json
from tMsgText import tMsgText
from tMsgSender import tMsgSender
from config import Config

class Test_regexParse(unittest.TestCase):
    def setUp(self) -> None:
        self.conf = Config
        self.tSender = tMsgSender("12345678")

    def test_validURLs(self) -> None:
        url: str = "https://twitter.com/testUser/status/1234567898765432123"
        msg = json.loads('{"message_id": 1, "from": {"id": 12345678, "is_bot": false, "first_name": "test_fName", "username": "test_username", "language_code": "en"}, "chat": {"id": 12345678, "first_name": "test_fName", "username": "test_username", "type": "private"}, "date": 1234567890, "text": "https://twitter.com/testUser/status/1234567898765432123", "entities": [{"offset": 0, "length": 55, "type": "url"}]}')

        tMsg: tMsgText = tMsgText(msg, self.tSender, self.conf)
        parsedRegex: list[str] = tMsg.parseRegex(msg['text'])

        self.assertEqual([url], parsedRegex)


if __name__ == '__main__':
    unittest.main()
