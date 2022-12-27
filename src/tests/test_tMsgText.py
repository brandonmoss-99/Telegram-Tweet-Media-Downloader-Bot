import unittest, json
from tMsgText import tMsgText
from tMsgSender import tMsgSender
from config import Config

class Test_regexParse(unittest.TestCase):
    def setUp(self) -> None:
        self.conf = Config()
        self.tSender = tMsgSender("12345678")

    def test_validURLs(self) -> None:
        urls: list[tuple[str, str]] = [
            ("http://twitter.com/testUser/status/1234567898765432122", "http://twitter.com/testUser/status/1234567898765432122"),
            ("https://twitter.com/testUser/status/1234567898765432123", "https://twitter.com/testUser/status/1234567898765432123"),
            ("https://twitter.com/test_User/status/1234567898765432124", "https://twitter.com/test_User/status/1234567898765432124"),
            ("https://twitter.com/testUser/status/1234567898765432125?s=12&t=123456789", "https://twitter.com/testUser/status/1234567898765432125"),
            ("https://twitter.com/test_User/status/1234567898765432126?s=12&t=123456789", "https://twitter.com/test_User/status/1234567898765432126"),
            ("https://twitter.com/test_User12345/status/1234567898765432127?s=12&t=123456789", "https://twitter.com/test_User12345/status/1234567898765432127"),
            ("https://vxtwitter.com/test_User12345/status/1234567898765432127?s=12&t=123456789", "https://vxtwitter.com/test_User12345/status/1234567898765432127"),
            ("https://fxtwitter.com/test_User12345/status/1234567898765432127?s=12&t=123456789", "https://fxtwitter.com/test_User12345/status/1234567898765432127"),
        ]
        for url in urls:
            msg = json.loads(f'{{"message_id": 1, "from": {{"id": 12345678, "is_bot": false, "first_name": "test_fName", "username": "test_username", "language_code": "en"}}, "chat": {{"id": 12345678, "first_name": "test_fName", "username": "test_username", "type": "private"}}, "date": 1234567890, "text": "{url[0]}"}}')
            tMsg: tMsgText = tMsgText(msg, self.tSender, self.conf)
            parsedRegex: list[str] = tMsg.parseRegex(msg['text'])
            self.assertEqual([url[1]], parsedRegex)

    def test_invalidURLs(self) -> None:
        urls: list[str] = [
            "smb://example.com/something",
            "test://example.com/something",
            "test://twitter.com/test_User12345/status/1234567898765432127?s=12&t=123456789"
        ]
        for url in urls:
            msg = json.loads(f'{{"message_id": 1, "from": {{"id": 12345678, "is_bot": false, "first_name": "test_fName", "username": "test_username", "language_code": "en"}}, "chat": {{"id": 12345678, "first_name": "test_fName", "username": "test_username", "type": "private"}}, "date": 1234567890, "text": "{url}"}}')
            tMsg: tMsgText = tMsgText(msg, self.tSender, self.conf)
            parsedRegex: list[str] = tMsg.parseRegex(msg['text'])
            self.assertEqual([], parsedRegex)


class Test_getInfo(unittest.TestCase):
    def setUp(self) -> None:
        self.conf = Config()
        self.tSender = tMsgSender("12345678")

    def test_getInfo(self) -> None:
        msg = json.loads(f'{{"message_id": 1, "from": {{"id": 12345678, "is_bot": false, "first_name": "test_fName", "username": "test_username", "language_code": "en"}}, "chat": {{"id": 12345678, "first_name": "test_fName", "username": "test_username", "type": "private"}}, "date": 1234567890, "text": "testText"}}')
        tMsg: tMsgText = tMsgText(msg, self.tSender, self.conf)
        self.assertEqual(tMsg.message_id, 1)
        self.assertEqual(tMsg.date, 1234567890)
        self.assertEqual(tMsg.chat, json.loads('{"id": 12345678, "first_name": "test_fName", "username": "test_username", "type": "private"}'))
        self.assertEqual(tMsg.isfrom, json.loads('{"id": 12345678, "is_bot": false, "first_name": "test_fName", "username": "test_username", "language_code": "en"}'))


class Test_IDAllowDeny(unittest.TestCase):
    def setUp(self) -> None:
        self.conf = Config()
        self.allowedIds = [123456, 1234567, 0, -99999999]
        self.conf.setAllowedIds(self.allowedIds)
        self.tSender = tMsgSender("12345678")
        
    def test_allowedIds(self) -> None:
        for id in self.allowedIds:
            msg = json.loads(f'{{"message_id": 1, "from": {{"id": {id}, "is_bot": false, "first_name": "test_fName", "username": "test_username", "language_code": "en"}}, "chat": {{"id": 12345678, "first_name": "test_fName", "username": "test_username", "type": "private"}}, "date": 1234567890, "text": "testText"}}')
            tMsg: tMsgText = tMsgText(msg, self.tSender, self.conf)
            self.assertEqual(tMsg.checkCanReply(id), True)
    
    def test_invalidIds(self) -> None:
        notAllowedIds = [123457, 1234568, -1234]

        for id in notAllowedIds:
            msg = json.loads(f'{{"message_id": 1, "from": {{"id": {id}, "is_bot": false, "first_name": "test_fName", "username": "test_username", "language_code": "en"}}, "chat": {{"id": 12345678, "first_name": "test_fName", "username": "test_username", "type": "private"}}, "date": 1234567890, "text": "testText"}}')
            tMsg: tMsgText = tMsgText(msg, self.tSender, self.conf)
            self.assertEqual(tMsg.checkCanReply(id), False)


if __name__ == '__main__':
    unittest.main()
