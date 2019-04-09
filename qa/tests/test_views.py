from django.test import TestCase, Client
from users.models import CustomUser
from qa.models import Question, Answer, Category
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

    def test_get_by_auth_id_template(self):
        response = self.client.get(reverse('author', kwargs={'a_id': self.user.id}))
        self.assertTemplateUsed(response, 'qa/questions.html')


class SignUpLogInViewTests(TestCase):

    def test_signup_page(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign Up')

    def test_signup_template_used(self):
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'signup.html')

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log In')

    def test_login_page_template(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'registration/login.html')


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

    def test_answer_exists_and_template(self):
        self.assertContains(self.response, self.answer.text)

    def test_answer_template_used(self):
        self.assertTemplateUsed(self.response, 'qa/answer.html')


class CategoryViewTest(TestCase):

    def setUp(self):

        self.user = CustomUser.objects.create_user(
            username='ruslan',
            email='testuser@test.com',
            password='secret_password'
        )

        self.category = Category.objects.create(
            name='Main Category',
            slug='test_category',
            description='This is test category description',
        )

    def test_all_categories_url(self):
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, 200)

    def test_all_categories_body(self):
        response = self.client.get(reverse('categories'))
        self.assertContains(response, 'Main Category')

    def test_all_categories_template(self):
        response = self.client.get(reverse('categories'))
        self.assertTemplateUsed(response, 'qa/categories.html')

    def test_single_category_url(self):
        response = self.client.get(reverse('category', kwargs={'a_id': self.category.id}))
        self.assertEqual(response.status_code, 200)

    def test_single_category_body(self):
        response = self.client.get(reverse('category', kwargs={'a_id': self.category.id}))
        self.assertContains(response, 'Main Category')

    def test_create_category_url_no_login(self):
        response = self.client.get(reverse('create_category'))
        self.assertEqual(response.status_code, 302)

    def test_create_category_url_logged_in(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(reverse('create_category'), follow=True)
        self.assertEqual(response.status_code, 200)




