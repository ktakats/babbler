from channels import Channel
from channels.test import ChannelTestCase

class ChatTest(ChannelTestCase):

    def test_basic(self):
        Channel("websocket.receive").send({"bla": "bla"})