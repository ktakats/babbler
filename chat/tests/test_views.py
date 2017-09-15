from django.test import TestCase

class HomeViewTest(TestCase):

    def test_view_uses_home_template(self):
        response=self.client.get('/')
        self.assertTemplateUsed(response, 'chat/home.html')


class ChatRoomViewTest(TestCase):

    def test_view_uses_chat_template(self):
        response = self.client.get('/room/main/')
        self.assertTemplateUsed(response, 'chat/chat.html')

