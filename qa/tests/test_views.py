from django.test import TestCase
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

    def test_popular_status_code(self):
        response = self.client.get('/popular/')
        self.assertEqual(response.status_code, 200)
