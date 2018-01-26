from django.test import TestCase
from chat.models import Room, Message
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from friendship.models import Friend, FriendshipRequest
from datetime import datetime, timedelta
from django.utils import timezone
import mock

User=get_user_model()

def create_and_log_in_user(self, email='bla@bla.com', password='bla', first_name='Test'):
    user=User.objects.create_user(email=email, password=password, first_name=first_name)
    self.client.force_login(user)
    return user

def create_room(user, title='NewRoom'):
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
        user=User.objects.create_user(email='bla@bla.com', password='bla', first_name='Test')
        room=create_room(user)
        response=self.client.get('/')
        self.assertNotContains(response, room.title)

    def test_view_doesnot_show_link_to_create_room(self):
        response = self.client.get('/')
        self.assertNotContains(response, 'Create a new room')

    #logged in

    def test_page_shows_existing_rooms(self):
        user=create_and_log_in_user(self)
        group1 = Group.objects.create(name='room1')
        room1=Room.objects.create(title="Room1", group=group1)
        group2 = Group.objects.create(name='room2')
        room2=Room.objects.create(title="Room2", group=group2)
        group1.user_set.add(user)
        group2.user_set.add(user)
        response=self.client.get('/')
        self.assertContains(response, room1.title)
        self.assertContains(response, room2.title)

    def test_includes_route_to_creating_new_room(self):
        create_and_log_in_user(self)
        response=self.client.get('/')
        self.assertContains(response, 'fa-plus')

    def test_view_shows_if_theres_request(self):
        user=create_and_log_in_user(self)
        second_user=User.objects.create_user(email='bla2@bla.com', password='blabla', first_name='Bla')
        Friend.objects.add_friend(second_user, user)
        response=self.client.get('/')
        self.assertContains(response, 'fa-envelope-o')

    def test_view_only_shows_room_where_user_belongs(self):
        user = create_and_log_in_user(self)
        second_user = User.objects.create_user(email='bla2@bla.com', password='bla', first_name='Test')
        third_user = User.objects.create_user(email='bla3@bla.com', password='blabla', first_name='Third')
        group = Group.objects.create(name='test')
        room = Room.objects.create(title='test', group=group)
        group.user_set.add(second_user)
        group.user_set.add(third_user)
        response = self.client.get('/')
        self.assertNotContains(response, room.title)

    def test_view_shows_author_and_time_of_last_message_in_room(self):
        user = create_and_log_in_user(self)
        second_user = User.objects.create_user(email='bla2@bla.com', password='bla', first_name='Bob')
        third_user = User.objects.create_user(email='bla3@bla.com', password='bla', first_name='Cec')
        room1 = create_room(user)
        room2 = create_room(user, title="Second room")
        msg1 = Message.objects.create(text='test message', author=second_user, room=room1)
        msg2 =  Message.objects.create(text='test message', author=third_user, room=room2)
        response=self.client.get('/')
        self.assertContains(response, msg1.author.first_name)
        self.assertContains(response, msg2.author.first_name)

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
        self.assertRedirects(response, '/room/%d/' % room.id)

    def test_view_requires_login(self):
        response=self.client.get('/new_room/')
        self.assertRedirects(response, '/?next=/new_room/')

    def test_only_the_friends_of_user_are_shown(self):
        user=create_and_log_in_user(self)
        second_user=User.objects.create_user(email='bla2@bla.com', password='bla', first_name='Test')
        third_user=User.objects.create_user(email='bla3@bla.com', password='blabla', first_name='Third')
        Friend.objects.create(from_user=user, to_user=second_user)
        response=self.client.get('/new_room/')
        self.assertContains(response, second_user.first_name)
        self.assertNotContains(response, third_user.first_name)

class ChatRoomViewTest(TestCase):

    def test_view_uses_chat_template(self):
        user=create_and_log_in_user(self)
        room=create_room(user)
        response = self.client.get('/room/'+str(room.id)+'/')
        self.assertTemplateUsed(response, 'chat/chat.html')

    def test_view_requires_login(self):
        user = create_and_log_in_user(self)
        room = create_room(user)
        self.client.logout()
        response = self.client.get('/room/%d/' % room.id)
        self.assertRedirects(response, '/?next=/room/%d/' % room.id)

    def test_view_renders_message_form(self):
        user = create_and_log_in_user(self)
        room = create_room(user)
        response = self.client.get('/room/' + str(room.id) + '/')
        self.assertContains(response, 'id_text')

    def test_submitting_form_creates_new_message(self):
        user = create_and_log_in_user(self)
        room = create_room(user)
        self.client.post('/room/' + str(room.id) + '/', data={'text': 'test', 'author': user})
        msg=Message.objects.first()
        self.assertEqual(msg.text, 'test')

    def test_view_shows_previously_sent_messages(self):
        user = create_and_log_in_user(self)
        room = create_room(user)
        msg=Message.objects.create(text='test message', author=user, room=room)
        response=self.client.get('/room/'+str(room.id)+'/')
        self.assertContains(response, 'test message')

    def test_messages_show_author_and_time(self):
        user = create_and_log_in_user(self)
        room = create_room(user)
        msg = Message.objects.create(text='test message', author=user, room=room)
        response = self.client.get('/room/%d/' % room.id)
        self.assertContains(response, user.first_name)
        self.assertContains(response, 'minutes ago')

    def test_message_created_more_than_an_hour_ago_shows_day_and_time(self):
        user = create_and_log_in_user(self)
        room = create_room(user)

        testtime = timezone.now() - timedelta(hours=1,minutes=30)
        # need to use mock, because pub_date has auto_add_now
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = testtime
            msg = Message.objects.create(text='test message', author=user, room=room)
        response = self.client.get('/room/%d/' % room.id)
        self.assertContains(response, user.first_name)
        self.assertContains(response, msg.pub_date.strftime("%a %H:%M"))


    def test_message_created_more_than_a_week_ago_shows_date_and_time(self):
        user = create_and_log_in_user(self)
        room = create_room(user)
        testtime = timezone.now() - timedelta(weeks=1, minutes=30)
        # need to use mock, because pub_date has auto_add_now
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = testtime
            msg = Message.objects.create(text='test message', author=user, room=room)
        response = self.client.get('/room/%d/' % room.id)
        self.assertContains(response, user.first_name)
        self.assertContains(response, msg.pub_date.strftime("%b %d %H:%M"))

    def test_message_created_more_than_a_year_ago_shows_year(self):
        user = create_and_log_in_user(self)
        room = create_room(user)

        testtime = timezone.now() - timedelta(weeks=53, minutes=30)
        # need to use mock, because pub_date has auto_add_now
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = testtime
            msg = Message.objects.create(text='test message', author=user, room=room)
        response = self.client.get('/room/%d/' % room.id)
        self.assertContains(response, user.first_name)
        self.assertContains(response, msg.pub_date.strftime("%b %d %Y %H:%M"))

    def test_only_group_members_can_see_view(self):
        user=create_and_log_in_user(self)
        second_user=User.objects.create_user(email='bla2@bla.com', password='blabla', first_name='Bla')
        third_user=User.objects.create_user(email='bla3@bla.com', password='blablabla', first_name='NON')
        group=Group.objects.create(name='test')
        room=Room.objects.create(title='test', group_id=group.id)
        group.user_set.add(second_user)
        group.user_set.add(third_user)
        response=self.client.get('/room/%d/' % room.id)
        self.assertRedirects(response, '/')

    def test_view_lists_all_the_rooms_of_user(self):
        user = create_and_log_in_user(self)
        second_user = User.objects.create_user(email='bla2@bla.com', password='blabla', first_name='Bla')
        group = Group.objects.create(name='test')
        room1 = Room.objects.create(title='Room1', group=group)
        room2 = Room.objects.create(title='TestRoom', group=group)
        room3 = create_room(second_user, "Third room")
        group.user_set.add(user)
        group.user_set.add(second_user)
        msg = Message.objects.create(text="Blablalba bla", author=second_user, room=room2)
        response = self.client.get('/room/%d/' % room1.id)
        self.assertContains(response, room2.title)
        self.assertNotContains(response, room3.title)
        self.assertContains(response, msg.author)

    def test_view_does_not_list_current_room(self):
        user = create_and_log_in_user(self)
        second_user = User.objects.create_user(email='bla2@bla.com', password='blabla', first_name='Bla')
        group = Group.objects.create(name='test')
        room1 = Room.objects.create(title='Room1', group=group)
        room2 = Room.objects.create(title='TestRoom', group=group)
        group.user_set.add(user)
        group.user_set.add(second_user)
        response = self.client.get('/room/%d/' % room1.id)
        self.assertNotIn(room1, response.context['all_rooms'])

    def test_list_ordered_by_last_msg_date(self):
        user = create_and_log_in_user(self)
        second_user = User.objects.create_user(email='bla2@bla.com', password='blabla', first_name='Bla')
        group = Group.objects.create(name='test')
        room1 = Room.objects.create(title='Room1', group=group)
        room2 = Room.objects.create(title='TestRoom', group=group)
        room3 = Room.objects.create(title='Third room', group=group)
        group.user_set.add(user)
        group.user_set.add(second_user)

        testtime1 = timezone.now() - timedelta(hours=1, minutes=20)
        testtime2 = timezone.now() - timedelta(hours=1, minutes=30)
        # need to use mock, because pub_date has auto_add_now
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = testtime1
            msg1 = Message.objects.create(text='test message 1', author=user, room=room2)
            mock_now.return_value = testtime2
            msg2 = Message.objects.create(text='test message 2', author=user, room=room3)

        response = self.client.get('/room/%d/' % room1.id)
        self.assertEquals(response.context['all_rooms'][0], room2)



class FindFriendsViewTest(TestCase):

    def test_view_uses_findfriends_template(self):
        user=create_and_log_in_user(self)
        response=self.client.get('/find_friends/')
        self.assertTemplateUsed(response, 'chat/find_friends.html')

    def test_view_renders_form(self):
        user=create_and_log_in_user(self)
        response = self.client.get('/find_friends/')
        self.assertContains(response, 'email')

    def test_searching_for_email_returns_user(self):
        user=create_and_log_in_user(self)
        response=self.client.get('/find_friends/', data={'email': user.email})
        self.assertContains(response, user.first_name)

    def test_searching_for_nonexistent_email_returns_noresult(self):
        user=create_and_log_in_user(self)
        response = self.client.get('/find_friends/', data={'email': 'bla2@bla.com'})
        self.assertContains(response, 'No result')

    def test_has_to_validate_email(self):
        user =create_and_log_in_user(self)
        response = self.client.get('/find_friends/', data={'email': 'vla.com'})
        self.assertContains(response, 'Not a valid email')

    def test_requires_login(self):
        user = User.objects.create_user(email='bla@bla.com', password='blabla', first_name='Test')
        response = self.client.get('/find_friends/')
        self.assertRedirects(response, '/?next=/find_friends/')

    def test_invite_creates_friend_request(self):
        user=create_and_log_in_user(self)
        second_user=User.objects.create_user(email='bla2@bla.com', password='blabla', first_name='Bla')
        response=self.client.get('/find_friends/', data={'invite': second_user.id})
        f=FriendshipRequest.objects.first()
        self.assertEquals(f.from_user.id, user.id)
        self.assertEquals(f.to_user.id, second_user.id)
        self.assertContains(response, 'Invite sent to '+ second_user.first_name + '!')

class MessagesViewTest(TestCase):

    def test_view_uses_messages_template(self):
        user=create_and_log_in_user(self)
        response=self.client.get('/pm/')
        self.assertTemplateUsed(response, 'chat/messages.html')

    def test_view_requires_login(self):
        response = self.client.get('/pm/')
        self.assertRedirects(response, '/?next=/pm/')

    def test_view_shows_pending_friend_requests(self):
        user=create_and_log_in_user(self)
        second_user = User.objects.create_user(email='bla2@bla.com', password='blabla', first_name='Bla')
        Friend.objects.add_friend(second_user, user, message=second_user.first_name + ' wants to connect')
        response=self.client.get('/pm/')
        self.assertContains(response, second_user.first_name)
        self.assertContains(response, 'Accept')
        self.assertContains(response, 'Decline')

    def test_accepting_request_creates_friendship(self):
        user = create_and_log_in_user(self)
        second_user = User.objects.create_user(email='bla2@bla.com', password='blabla', first_name='Bla')
        third_user=User.objects.create_user(email='bla3@bla.com', password='blabla', first_name='Joe')
        Friend.objects.add_friend(second_user, user, message=second_user.first_name + ' wants to connect')
        Friend.objects.add_friend(third_user, user, message=third_user.first_name + ' wants to connect')
        f=FriendshipRequest.objects.get(from_user_id=second_user.id)
        response=self.client.post('/pm/', data={'accept': f.id})
        self.assertEquals(Friend.objects.count(), 2)
        self.assertNotContains(response, second_user.first_name)

    def test_declining_request_doesnot_create_friendship(self):
        user = create_and_log_in_user(self)
        second_user = User.objects.create_user(email='bla2@bla.com', password='blabla', first_name='Bla')
        third_user = User.objects.create_user(email='bla3@bla.com', password='blabla', first_name='Joe')
        Friend.objects.add_friend(second_user, user, message=second_user.first_name + ' wants to connect')
        Friend.objects.add_friend(third_user, user, message=third_user.first_name + ' wants to connect')
        f = FriendshipRequest.objects.get(from_user_id=second_user.id)
        response = self.client.post('/pm/', data={'decline': f.id})
        self.assertEquals(Friend.objects.count(), 0)
        self.assertNotContains(response, second_user.first_name)

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

