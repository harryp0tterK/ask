from django.test import TestCase
from django.urls import reverse


class CreateQuestionTest(TestCase):
    data = {'text': 'testText', 'title': 'testTitle'}

    def test_try_to_post_with_no_login(self):
        response = self.client.post(reverse('ask'), self.data)
        self.assertEqual(response.status_code, 302)
