from django.test import TestCase

class ChatViewTest(TestCase):

    def test_view_uses_chat_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'chat/chat.html')