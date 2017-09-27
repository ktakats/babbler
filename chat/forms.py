from django import forms
from .models import Room, Message
from django.contrib.auth import get_user_model, authenticate

User=get_user_model()

class NewRoomForm(forms.models.ModelForm):

    class Meta:
        model=Room
        fields=['title']
        labels={'title': ''}
        widgets={
            'title': forms.TextInput(attrs={'placeholder': 'Add a new room'})
        }

    def save(self):
        data=self.cleaned_data
        room=Room.objects.create(title=data['title'])
        return room

class MsgForm(forms.models.ModelForm):

    class Meta:
        model=Message
        fields=['text']
        labels={'text': ''}

    def save(self, author, room):
        data=self.cleaned_data
        msg=Message.objects.create(text=data['text'], author=author, room=room)
        return msg

class SignupForm(forms.models.ModelForm):
    password1=forms.CharField(label='Password', widget=forms.PasswordInput)
    password2=forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=('email', 'first_name')

    def clean(self):
        cleaned_data=super(SignupForm, self).clean()
        pw1=cleaned_data['password1']
        pw2=cleaned_data['password2']
        if pw1 and pw2 and pw1 != pw2:
            msg="Passwords do not match"
            self.add_error('password2', msg)

    def save(self):
        data=self.cleaned_data
        user=User(email=data['email'], first_name=data['first_name'])
        user.set_password(data["password1"])
        user.save()
        return user

class LoginForm(forms.models.ModelForm):

    class Meta:
        model=User
        fields=('email', 'password')
        widgets={
            'password': forms.PasswordInput()
        }

    def clean(self):
        email=self.cleaned_data.get('email')
        password=self.cleaned_data.get('password')
        user=authenticate(email=email, password=password)
        if not user or not user.is_active:
            msg="Login is invalid. Please try again"
            self.add_error('email', msg)

