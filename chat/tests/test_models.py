from django.test import TestCase
from chat.models import Room

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
