from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=30)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class ProfileForm(forms.Form):
    picture = forms.ImageField()


class ContactForm(forms.Form):
    email_sending = forms.EmailField(required=True)


class ImageUploadForm(forms.Form):
    image = forms.ImageField()

