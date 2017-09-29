from django.test import TestCase
from chat.models import Room, Message
from django.contrib.auth import get_user_model

User=get_user_model()

def create_and_log_in_user(self, email='bla@bla.com', password='bla', first_name='Test'):
    user=User.objects.create_user(email=email, password=password, first_name=first_name)
    self.client.force_login(user)
    return user


class HomeViewTest(TestCase):

    #not logged in

    def test_view_uses_home_template(self):
        response=self.client.get('/')
        self.assertTemplateUsed(response, 'chat/home.html')

    def test_view_renders_login_form(self):
        response=self.client.get('/')
        self.assertContains(response, 'id_email')
        self.assertContains(response, 'id_password')

    def test_logging_in_redirects_to_home(self):
        user=User.objects.create_user(email='bla@bla.com', password='bla', first_name='Test')
        response=self.client.post('/', data={'email': 'bla@bla.com', 'password': 'bla'})
        self.assertRedirects(response, '/')

    def test_view_has_signup(self):
        response = self.client.get('/')
        self.assertContains(response, 'Sign up')

    #logged in

    def test_view_renders_new_room_form_when_user_logged_in(self):
        create_and_log_in_user(self)
        response = self.client.get('/')
        self.assertContains(response, 'id_title')

    def test_submitting_form_creates_new_room(self):
        create_and_log_in_user(self)
        self.client.post('/', data={'title': 'Main'})
        room=Room.objects.first()
        self.assertEqual(room.title, 'Main')

    def test_creating_room_redirects_to_room(self):
        create_and_log_in_user(self)
        response=self.client.post('/', data={'title': 'Main'})
        room = Room.objects.first()
        self.assertRedirects(response, '/room/%s/' % room.title)

class ChatRoomViewTest(TestCase):

    def test_view_uses_chat_template(self):
        create_and_log_in_user(self)
        room=Room.objects.create(title='main')
        response = self.client.get('/room/main/')
        self.assertTemplateUsed(response, 'chat/chat.html')

    def test_view_requires_login(self):
        room=Room.objects.create(title='main')
        response = self.client.get('/room/main/')
        self.assertRedirects(response, '/?next=/room/main/')

    def test_view_renders_message_form(self):
        create_and_log_in_user(self)
        room = Room.objects.create(title='main')
        response = self.client.get('/room/main/')
        self.assertContains(response, 'id_text')

    def test_submitting_form_creates_new_message(self):
        user=create_and_log_in_user(self)
        room = Room.objects.create(title='main')
        self.client.post('/room/main/', data={'text': 'test', 'author': user})
        msg=Message.objects.first()
        self.assertEqual(msg.text, 'test')

    def test_view_shows_previously_sent_messages(self):
        user = create_and_log_in_user(self)
        room = Room.objects.create(title='main')
        msg=Message.objects.create(text='test message', author=user, room=room)
        response=self.client.get('/room/main/')
        self.assertContains(response, 'test message')

    def test_messages_show_author_and_time(self):
        user = create_and_log_in_user(self)
        room = Room.objects.create(title='main')
        msg = Message.objects.create(text='test message', author=user, room=room)
        response = self.client.get('/room/main/')
        self.assertContains(response, user.first_name)
        self.assertContains(response, msg.pub_date.strftime("%d, %Y"))

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
        create_and_log_in_user(self)
        response=self.client.get('/accounts/logout/')
        self.assertRedirects(response, '/')

