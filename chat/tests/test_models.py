from django.test import TestCase
from chat.models import Room, Message
from django.contrib import auth
from django.contrib.auth.models import Group
import time

User=auth.get_user_model()

def create_room(title='main'):
    group=Group.objects.create(name=title)
    room=Room.objects.create(title=title, group=group)
    return room


class RoomModelTest(TestCase):

    def test_default_test(self):
        room=Room()
        self.assertEqual(room.title, '')

    def test_can_create_room(self):
        room=create_room()
        self.assertEqual(Room.objects.first(), room)

    def test_room_has_absolute_url(self):
        room = create_room()
        self.assertEqual(room.get_absolute_url(), '/room/%d/' % (room.id))

    def test_filtering_by_user_group(self):
        user = User.objects.create_user(email='bla@bla.com', password='bla', first_name='Test')
        room = create_room()
        group = Group.objects.first()
        group.user_set.add(user)
        filtered = Room.objects.get_group_rooms(user)
        self.assertEquals(room, filtered.first())

    def test_last_msg_date_updated_with_new_msg(self):
        user = User.objects.create_user(email='bla@bla.com', password='bla', first_name='Test')
        room = create_room()
        msg1 = Message.objects.create(text="First message", author=user, room=room)
        self.assertEquals(room.last_msg_date, msg1.pub_date)
        time.sleep(10)
        msg2 = Message.objects.create(text="Second message", author=user, room=room)
        self.assertEquals(room.last_msg_date, msg2.pub_date)



class UserModelTest(TestCase):

    def test_can_create_user(self):
        user=User.objects.create_user(email='bla@bla.com', password='blabla', first_name="Test")
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first(), user)

class MessageModelTest(TestCase):

    def test_can_create_message(self):
        user=User.objects.create_user(email='bla@bla.com', password='bla', first_name='Test')
        room=create_room()
        msg=Message.objects.create(text="First message", author=user, room=room)
        self.assertEqual(Message.objects.count(), 1)

