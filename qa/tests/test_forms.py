from django.test import TestCase
from django.shortcuts import reverse
from users.models import CustomUser
from qa.models import Question


class CreateQuestionTest(TestCase):

    def setUp(self):

        self.user = CustomUser.objects.create_user(
            username='ruslan',
            email='testuser@test.com',
            password='secret_password'
        )

        self.question = Question.objects.create(
            title='A good title',
            text='Nice body content, Lorem Ipsum',
            author=self.user,
        )

        self.data = {'text': 'Nice body content, Lorem Ipsum', 'title': 'A good title'}

    def test_try_to_ask_no_login(self):
        response = self.client.post(reverse('ask'), self.data)
        self.assertRedirects(response, '/accounts/login/?next=/ask/')

    def test_try_to_answer_no_login(self):
        response = self.client.post(self.question.get_url(), self.data, follow=True)
        self.assertContains(response, 'login')

    def test_login_and_ask_question(self):
        self.client.login(username=self.user.username, password='secret_password')
        response = self.client.post(reverse('ask'), self.data, follow=True)
        self.assertContains(response, self.data['text'])

    def test_login_and_answer(self):
        self.client.login(username=self.user.username, password='secret_password')
        response = self.client.post(self.question.get_url(), self.data, follow=True)
        self.assertContains(response, self.data['text'])

