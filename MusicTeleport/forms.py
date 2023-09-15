from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.PasswordInput()


class PlaylistSelectForm(forms.Form):
    def __init__(self, playlist_choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['selected_playlist'] = forms.ChoiceField(
            choices=playlist_choices,
            widget=forms.RadioSelect
        )
