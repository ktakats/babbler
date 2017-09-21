from django.test import TestCase
from chat.forms import NewRoomForm
from chat.models import Room

class NewRoomFormTest(TestCase):

    def test_form_has_placeholders(self):
        form=NewRoomForm()
        self.assertIn('Add a new room', form.as_p())

    def test_form_validation(self):
        form=NewRoomForm(data={'title': 'main'})
        self.assertTrue(form.is_valid())