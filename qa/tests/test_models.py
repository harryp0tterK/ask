from users.models import CustomUser
from django.test import TestCase
from django.urls import reverse


class SignupUserTests(TestCase):

    def test_signup(self):
        new_user = CustomUser.objects.create_user(
            username='ruslan',
            email='testuser@test.com',
            password='secret_password'
        )

        self.assertEqual(CustomUser.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all()[0].username, new_user.username)