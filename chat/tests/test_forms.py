from django.test import TestCase
from chat.forms import NewRoomForm, SignupForm
from chat.models import Room
from django.contrib import auth

User=auth.get_user_model()

class NewRoomFormTest(TestCase):

    def test_form_has_placeholders(self):
        form=NewRoomForm()
        self.assertIn('Add a new room', form.as_p())

    def test_form_validation(self):
        form=NewRoomForm(data={'title': 'main'})
        self.assertTrue(form.is_valid())

class SignupFormTest(TestCase):

    def test_form_has_placeholders(self):
        form=SignupForm()
        self.assertIn('email', form.as_p())

    def test_form_validation(self):
        form=SignupForm(data={'email': 'bla@bla.com', 'password1': 'bla', 'password2': 'bla', 'first_name': 'Test'})
        self.assertTrue(form.is_valid())

    def test_form_passwords_have_to_be_the_same(self):
        form = SignupForm(data={'email': 'bla@bla.com', 'password1': 'bla', 'password2': 'blabla', 'first_name': 'Test'})
        self.assertFalse(form.is_valid())

    def test_submitting_form_saves_user(self):
        form = SignupForm(data={'email': 'bla@bla.com', 'password1': 'bla', 'password2': 'bla', 'first_name': 'Test'})
        self.assertTrue(form.is_valid())
        form.save()
        user=User.objects.first()
        self.assertEqual(user.email, 'bla@bla.com')