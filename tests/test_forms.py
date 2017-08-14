from wheretoeat.models import *
from django.test import TestCase
from wheretoeat.forms import *


class SetUpClass(TestCase):
    def setup(self):
        self.user = UserProfile.objects.create(username="username", email="user@test.com", first_name="first", last_name="last", password1="elif6615", password2="elif6615")


class SignUpForm_Test(TestCase):
    def test_SignUpForm_valid(self):
        form = SignUpForm(data={'username': "username", 'email': "user@test.com", 'first_name': "first", 'last_name': "last", 'password1': "elif6615", 'password2': "elif6615"})
        self.assertTrue(form.is_valid())

    def test_SignUpForm_invalid(self):
        form = SignUpForm(data={'username': "username", 'email': "usertestcom", 'first_name': "first", 'last_name': "last", 'password1': "elif", 'password2': "elif"})
        self.assertFalse(form.is_valid())

