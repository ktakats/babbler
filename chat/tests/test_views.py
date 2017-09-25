from django.test import TestCase
from chat.models import Room
from django.contrib.auth import get_user_model

User=get_user_model()

class HomeViewTest(TestCase):

    def test_view_uses_home_template(self):
        response=self.client.get('/')
        self.assertTemplateUsed(response, 'chat/home.html')

    def test_view_renders_login_form(self):
        response=self.client.get('/')
        self.assertContains(response, 'id_email')
        self.assertContains(response, 'id_password')

    def test_view_renders_form(self):
        response = self.client.get('/')
        self.assertContains(response, 'id_title')

    def test_logging_in_redirects_to_home(self):
        user=User.objects.create_user(email='bla@bla.com', password='bla', first_name='Test')
        response=self.client.post('/', data={'email': 'bla@bla.com', 'password': 'bla'})
        self.assertRedirects(response, '/')
""""
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
"""

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

    def test_password_confirmation_fail_shows_error(self):
        response = self.client.post('/accounts/signup/', data={'email': 'bla@bla.com', 'password1': 'bla', 'password2': 'blabla','first_name': 'Test'})
        self.assertContains(response, "Passwords do not match")


class LogoutViewTest(TestCase):

    def test_logout(self):
        user=User.objects.create_user(email='bla@bla.com', password='bla', first_name='Test')
        self.client.force_login(user)
        response=self.client.get('/accounts/logout/')
        self.assertRedirects(response, '/')

class ChatRoomViewTest(TestCase):

    def test_view_uses_chat_template(self):
        room=Room.objects.create(title='main')
        response = self.client.get('/room/main/')
        self.assertTemplateUsed(response, 'chat/chat.html')

