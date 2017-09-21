from django import forms
from .models import Room

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