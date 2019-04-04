from django.db import models
from django.utils.text import slugify
from users.models import CustomUser


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-added_at')

    def popular(self):
        return self.order_by('-rating')


class QuestionCategoryManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    objects = QuestionCategoryManager()

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.slug

    def get_url(self):
        return f"/category/{self.id}"

    def get_number(self):
        # this method returns a related questions number
        c = Category.objects.annotate(num_questions=models.Count('question')).filter(id=self.id)
        return c[0].num_questions

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name) + str(self.id)
        super(Category, self).save(*args, **kwargs)


class Question(models.Model):
    title = models.CharField(blank=False, null=False, max_length=255)
    text = models.TextField()
    added_at = models.DateField(auto_now=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(CustomUser, on_delete=models.SET(value='Deleted'))
    likes = models.ManyToManyField(CustomUser, related_name='get_likes', default=0)
    category = models.ManyToManyField(Category, blank=True)

    # has_answer = models.BooleanField(default=False)

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def get_url(self):
        return f"/question/{self.id}"


class Answer(models.Model):
    added_at = models.DateField(auto_now=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.SET(value='Deleted'))
    text = models.TextField(null=True)

    active = models.BooleanField(default=True)  # added in case i'll need to deactivate some answers fsr
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies',
                               on_delete=models.CASCADE)  # deal with comments on answers

    # is_answer = models.BooleanField(Question, default=False, null=True, blank=True)
    # upvotes = models.IntegerField()

    def __str__(self):
        return self.text

