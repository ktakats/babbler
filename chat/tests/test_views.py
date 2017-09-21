from django.test import TestCase
from chat.models import Room

class HomeViewTest(TestCase):

    def test_view_uses_home_template(self):
        response=self.client.get('/')
        self.assertTemplateUsed(response, 'chat/home.html')

    def test_view_renders_form(self):
        response = self.client.get('/')
        self.assertContains(response, 'id_title')

    def test_submitting_form_creates_new_room(self):
        self.client.post('/', data={'title': 'Main'})
        room=Room.objects.first()
        self.assertEqual(room.title, 'Main')

    def test_creating_room_redirects_to_room(self):
        response=self.client.post('/', data={'title': 'Main'})
        room = Room.objects.first()
        self.assertRedirects(response, '/room/%s/' % room.title)

class ChatRoomViewTest(TestCase):

    def test_view_uses_chat_template(self):
        room=Room.objects.create(title='main')
        response = self.client.get('/room/main/')
        self.assertTemplateUsed(response, 'chat/chat.html')

