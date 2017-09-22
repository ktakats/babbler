from django.test import TestCase
from chat.models import Room
from django.contrib import auth

User=auth.get_user_model()

class RoomModelTest(TestCase):

    def test_default_test(self):
        room=Room()
        self.assertEqual(room.title, '')

    def test_can_create_room(self):
        room=Room.objects.create(title="main")
        self.assertEqual(Room.objects.first(), room)

    def test_room_has_absolute_url(self):
        room = Room.objects.create(title="main")
        self.assertEqual(room.get_absolute_url(), '/room/%s/' % (room.title))


class UserModelTest(TestCase):

    def test_can_create_user(self):
        user=User.objects.create_user(email='bla@bla.com', password='blabla', first_name="Test")
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first(), user)

