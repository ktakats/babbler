from django.test import TestCase
from chat.forms import MsgForm, NewRoomForm, SignupForm, LoginForm
from chat.models import Room
from django.contrib import auth

User=auth.get_user_model()

def create_and_log_in_user(self, email='bla@bla.com', password='bla', first_name='Test'):
    user=User.objects.create_user(email=email, password=password, first_name=first_name)
    self.client.force_login(user)
    return user

class NewRoomFormTest(TestCase):

    def test_form_has_placeholders(self):
        user=create_and_log_in_user(self)
        form=NewRoomForm(user)
        self.assertIn('Add a new room', form.as_p())

    def test_form_validation(self):
        user=create_and_log_in_user(self)
        form=NewRoomForm(user, data={'title': 'main'})
        self.assertTrue(form.is_valid())

    def test_form_lists_users(self):
        u=create_and_log_in_user(self)
        user = User.objects.create_user(email='bla2@bla.com', password='bla', first_name='Test_user')
        form=NewRoomForm(u)
        self.assertIn(user.first_name, form.as_p())

    def test_validation_with_user(self):
        u=create_and_log_in_user(self)
        user = User.objects.create_user(email='bla2@bla.com', password='bla', first_name='Test_user')
        form = NewRoomForm(u,data={'title': 'main', 'users': [user]})
        self.assertTrue(form.is_valid())

    def test_list_of_users_excludes_owner(self):
        user=create_and_log_in_user(self)
        second_user= User.objects.create_user(email='bla2@bla.com', password='blabla', first_name='Bla')
        form=NewRoomForm(user)
        self.assertIn(second_user.first_name, form.as_p())
        self.assertNotIn(user.first_name, form.as_p())

    def test_saving_form_creates_group_and_adds_users(self):
        user=create_and_log_in_user(self)
        second_user=User.objects.create_user(email='bla2@bla.com', password='blabla', first_name='Bla')
        third_user=User.objects.create_user(email='bla3@bla.com', password='blablabla', first_name='Bli')
        form=NewRoomForm(user, data={'title': 'main', 'users': [second_user, third_user]})
        form.is_valid()
        room=form.save()
        self.assertEqual(user.groups.count(),1)
        self.assertEqual(second_user.groups.count(), 1)
        self.assertEqual(third_user.groups.count(), 1)
        g=user.groups.first()
        self.assertEqual(g.name, room.title)

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