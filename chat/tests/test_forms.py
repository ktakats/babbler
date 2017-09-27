from django.test import TestCase
from chat.forms import MsgForm, NewRoomForm, SignupForm, LoginForm
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

class MsgFormTest(TestCase):

    def test_default_test(self):
        form=MsgForm()
        self.assertIn('id_text', form.as_p())

    def test_form_validation(self):
        user=User.objects.create_user(email='bla@bla.com', password='bla', first_name='Test_user')
        form=MsgForm(data={'text': 'Test', 'author': user})
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

    def test_form_has_error_message_if_passwords_donot_match(self):
        form = SignupForm(data={'email': 'bla@bla.com', 'password1': 'bla', 'password2': 'blabla', 'first_name': 'Test'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'][0], "Passwords do not match")

    def test_submitting_form_saves_user(self):
        form = SignupForm(data={'email': 'bla@bla.com', 'password1': 'bla', 'password2': 'bla', 'first_name': 'Test'})
        self.assertTrue(form.is_valid())
        form.save()
        user=User.objects.first()
        self.assertEqual(user.email, 'bla@bla.com')

class LoginFormTest(TestCase):

    def test_form_has_placeholders(self):
        form=LoginForm()
        self.assertIn('Email', form.as_p())
        self.assertIn('Password', form.as_p())

    def test_form_validation(self):
        user=User.objects.create_user(email='bla@bla.com', password='bla', first_name='Test')
        form=LoginForm(data={'email': 'bla@bla.com', 'password': 'bla'})
        self.assertTrue(form.is_valid())

    def test_form_error_for_wrong_password(self):
        user = User.objects.create_user(email='bla@bla.com', password='bla', first_name='Test')
        form = LoginForm(data={'email': 'bla@bla.com', 'password': 'blabla'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'][0], "Login is invalid. Please try again")