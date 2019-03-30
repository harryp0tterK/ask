from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import CustomUser
from qa.models import Question, Answer
from django.urls import reverse


class HomeViewTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='ruslan',
            email='testuser@test.com',
            password='secret_password'
        )

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
        self.assertContains(response, '<title>Most Popular</title>')

    def test_get_by_auth_id_status_code(self):
        response = self.client.get(reverse('author', kwargs={'a_id': self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/questions.html')


class QuestionViewTest(TestCase):

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

        self.answer = Answer.objects.create(
            question=self.question,
            author=self.user,
            text='Test Answer, should be fine!'

        )

        self.response = self.client.get(reverse('question', kwargs={'qn_id': self.question.id}))

    def test_question_url(self):
        self.assertEqual(self.response.status_code, 200)

    def test_question_template(self):
        self.assertTemplateUsed(self.response, 'qa/question.html')

    def test_question_title(self):
        self.assertContains(self.response, self.question.title)

    def test_author_link_exists(self):
        self.assertContains(self.response, f'author/{self.user.id}/')

    def test_answer(self):
        self.assertContains(self.response, self.answer.text)
        self.assertTemplateUsed(self.response, 'qa/answer.html')
