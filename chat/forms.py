from django import forms
from .models import Room
from django.contrib import auth

User=auth.get_user_model()

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
            raise forms.ValidationError("Passwords don't match")

    def save(self):
        data=self.cleaned_data
        user=User(email=data['email'], first_name=data['first_name'])
        user.set_password(data["password1"])
        user.save()
        return user

