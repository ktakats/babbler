from django.test import TestCase
from chat.models import Room, Message
from django.contrib import auth
from django.contrib.auth.models import Group

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

