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

    def test_view_has_signup(self):
        response = self.client.get('/')
        self.assertContains(response, 'Sign up')

class SignupViewTest(TestCase):

    def test_view_uses_signup_template(self):
        response=self.client.get('/accounts/signup/')
        self.assertTemplateUsed(response, 'chat/signup.html')

    def test_view_renders_form(self):
        response = self.client.get('/accounts/signup/')
        self.assertContains(response, 'id_email')

    def test_submitting_form_redirects_to_home(self):
        response=self.client.post('/accounts/signup/', data={'email': 'bla@bla.com', 'password1': 'bla', 'password2': 'bla', 'first_name': 'Test'})
        self.assertRedirects(response, '/')

class ChatRoomViewTest(TestCase):

    def test_view_uses_chat_template(self):
        room=Room.objects.create(title='main')
        response = self.client.get('/room/main/')
        self.assertTemplateUsed(response, 'chat/chat.html')

