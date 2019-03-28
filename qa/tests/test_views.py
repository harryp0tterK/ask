"""
Reminder! A Django test db is not a real db, it is a temporary instance
which is created when the test starts and destroyed after; nor does it have any actual User model data!
So in the test_get_by_auth_id_status_code I created a record manually.
"""

from django.test import TestCase, Client
from users.models import CustomUser
from django.urls import reverse


class HomeViewTests(TestCase):

    def test_home_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/questions.html')

    def test_home_contains_correct_html(self):
        response = self.client.get('/')
        self.assertContains(response, '<title>Main Page: Most Recent</title>')

    def test_popular_status_code(self):
        response = self.client.get('/popular/')
        self.assertEqual(response.status_code, 200)

    def test_popular_contains_correct_html(self):
        response = self.client.get('/popular/')
        self.assertContains(response, '<title>Main Page: Most Recent</title>')

    def test_get_by_auth_id_status_code(self):
        CustomUser(username='ruslan', password='pass').save()
        response = self.client.get(reverse('author', kwargs={'a_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/questions.html')
