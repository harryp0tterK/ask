from django.test import TestCase, Client
from django.urls import reverse


class CreateQuestionTest(TestCase):
    data = {'text': 'testText', 'title': 'testTitle'}

    def test_try_to_post_with_no_login(self):
        response = self.client.post(reverse('ask'), self.data)
        self.assertRedirects(response, '/accounts/login/?next=/ask/')

    def test_login(self):
        response = self.client.post('/users/login/', {'username': 'john', 'password': 'test'})
        self.assertEqual(response.status_code, 200)

    # def test_login_and_ask(self):
    #     # c = Client()
    #     self.client.login(username='fred', password='secret')
    #     r = self.client.post(reverse('ask'), self.data)
