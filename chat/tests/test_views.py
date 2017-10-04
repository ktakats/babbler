from django.test import TestCase
from chat.models import Room, Message
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User=get_user_model()

def create_and_log_in_user(self, email='bla@bla.com', password='bla', first_name='Test'):
    user=User.objects.create_user(email=email, password=password, first_name=first_name)
    self.client.force_login(user)
    return user

def create_room(user, title='main'):
    group=Group.objects.create(name=title)
    group.user_set.add(user)
    room=Room.objects.create(title=title, group_id=group.id)
    return room


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

    def test_view_doesnot_show_rooms(self):
        room=Room.objects.create(title="Room1")
        response=self.client.get('/')
        self.assertNotContains(response, 'Room1')

    def test_view_doesnot_show_link_to_create_room(self):
        response = self.client.get('/')
        self.assertNotContains(response, 'Create a new room')

    #logged in

    def test_page_shows_existing_rooms(self):
        create_and_log_in_user(self)
        room1=Room.objects.create(title="Room1")
        room2=Room.objects.create(title="Room2")
        response=self.client.get('/')
        self.assertContains(response, room1.title)
        self.assertContains(response, room2.title)

    def test_includes_route_to_creating_new_room(self):
        create_and_log_in_user(self)
        response=self.client.get('/')
        self.assertContains(response, 'Create a new room')

class NewRoomViewTest(TestCase):

    def test_view_renders_new_room_form(self):
        create_and_log_in_user(self)
        response = self.client.get('/new_room/')
        self.assertContains(response, 'id_title')

    def test_submitting_form_creates_new_room(self):
        create_and_log_in_user(self)
        self.client.post('/new_room/', data={'title': 'Main'})
        room = Room.objects.first()
        self.assertEqual(room.title, 'Main')

    def test_creating_room_redirects_to_room(self):
        create_and_log_in_user(self)
        response = self.client.post('/new_room/', data={'title': 'Main'})
        room = Room.objects.first()
        self.assertRedirects(response, '/room/%s/' % room.title)

    def test_view_requires_login(self):
        response=self.client.get('/new_room/')
        self.assertRedirects(response, '/?next=/new_room/')


class ChatRoomViewTest(TestCase):

    def test_view_uses_chat_template(self):
        user=create_and_log_in_user(self)
        room=create_room(user)
        response = self.client.get('/room/'+room.title+'/')
        self.assertTemplateUsed(response, 'chat/chat.html')

    def test_view_requires_login(self):
        user = create_and_log_in_user(self)
        room = create_room(user)
        self.client.logout()
        response = self.client.get('/room/'+room.title+'/')
        self.assertRedirects(response, '/?next=/room/main/')

    def test_view_renders_message_form(self):
        user = create_and_log_in_user(self)
        room = create_room(user)
        response = self.client.get('/room/' + room.title + '/')
        self.assertContains(response, 'id_text')

    def test_submitting_form_creates_new_message(self):
        user = create_and_log_in_user(self)
        room = create_room(user)
        self.client.post('/room/' + room.title + '/', data={'text': 'test', 'author': user})
        msg=Message.objects.first()
        self.assertEqual(msg.text, 'test')

    def test_view_shows_previously_sent_messages(self):
        user = create_and_log_in_user(self)
        room = create_room(user)
        msg=Message.objects.create(text='test message', author=user, room=room)
        response=self.client.get('/room/'+room.title+'/')
        self.assertContains(response, 'test message')

    def test_messages_show_author_and_time(self):
        user = create_and_log_in_user(self)
        room = create_room(user)
        msg = Message.objects.create(text='test message', author=user, room=room)
        response = self.client.get('/room/' + room.title + '/')
        self.assertContains(response, user.first_name)
        self.assertContains(response, msg.pub_date.strftime("%Y"))

    def test_only_group_members_can_see_view(self):
        user=create_and_log_in_user(self)
        second_user=User.objects.create_user(email='bla2@bla.com', password='blabla', first_name='Bla')
        third_user=User.objects.create_user(email='bla3@bla.com', password='blablabla', first_name='NON')
        group=Group.objects.create(name='test')
        room=Room.objects.create(title='test', group_id=group.id)
        group.user_set.add(second_user)
        group.user_set.add(third_user)
        response=self.client.get('/room/test/')
        self.assertRedirects(response, '/')

class FindFriendsViewTest(TestCase):

    def test_view_uses_findfriends_template(self):
        response=self.client.get('/find_friends/')
        self.assertTemplateUsed(response, 'chat/find_friends.html')

    def test_view_renders_form(self):
        response = self.client.get('/find_friends/')
        self.assertContains(response, 'id_email')

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

