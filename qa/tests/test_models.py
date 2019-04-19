from users.models import CustomUser
from qa.models import Question, Answer, Category
from django.test import TestCase


class SignupUserTests(TestCase):

    def test_signup(self):
        new_user = CustomUser.objects.create_user(
            username='ruslan',
            email='testuser@test.com',
            password='secret_password'
        )

        self.assertEqual(CustomUser.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all()[0].username, new_user.username)


class CategoryTests(TestCase):

    def setUp(self):

        self.c = Category.objects.create(
            name='TestCat',
            slug='test_cat',
            description='Creating New Category')

        self.u = CustomUser.objects.create_user(
            username='ruslan',
            email='testuser@test.com',
            password='secret_password'
        )

        self.q = Question.objects.create(
            title='A good title',
            text='Nice body content, Lorem Ipsum',
            author=self.u,
        )

    def test_create_category_and_str(self):
        self.assertEqual(Category.objects.all().count(), 1)
        self.assertEqual(Category.objects.all()[0].name, self.c.name)

    def test_get_natural_key(self):
        self.assertEqual(Category.objects.all()[0].natural_key(), self.c.slug)

    def test_get_category_url(self):
        self.assertEqual(Category.objects.all()[0].get_url(), self.c.get_url())

    def test_get_number_of_related_questions(self):
        self.assertEqual(Category.objects.all()[0].get_number(), 0)

    def test_get_number_of_related_questions_2(self):
        self.q.category.add(Category.objects.get(pk=1))
        self.assertEqual(Category.objects.all()[0].get_number(), 1)




