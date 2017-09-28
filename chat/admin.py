# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Room, User, Message

# Register your models here.
class UserCreationForm(forms.ModelForm):
    password1=forms.CharField(label='Password', widget=forms.PasswordInput)
    password2=forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=('email', 'first_name')

    def clean_password2(self):
        #check if the two password entries match
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        if password1 and password2 and password1!=password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        "save the password in hashed format"
        user=super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data("password1"))
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password=ReadOnlyPasswordHashField()

    class Meta:
        model=User
        fields=('email', 'password', 'first_name', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial['password']

class UserAdmin(BaseUserAdmin):

    form=UserChangeForm
    add_form=UserCreationForm

    list_display=('email', 'first_name', 'is_admin',)
    list_filter=('is_admin',)
    fieldsets=(
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets=(
        (None, {'classes': ('wide'), 'fields': ('email', 'first_name', 'password1', 'password2')}),
    )
    search_fields=('email',)
    ordering=('email',)
    filter_horizontal=()

admin.site.register(User, UserAdmin)
admin.site.register(Room)
admin.site.register(Message)

admin.site.unregister(Group)