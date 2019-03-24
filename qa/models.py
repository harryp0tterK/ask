from django.db import models
from users.models import CustomUser


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-added_at')

    def popular(self):
        return self.order_by('-rating')


class Question(models.Model):
    title = models.CharField(blank=False, null=False, max_length=255)
    text = models.TextField()
    added_at = models.DateField(auto_now=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(CustomUser, on_delete=models.SET(value='Deleted'))
    likes = models.ManyToManyField(CustomUser, related_name='get_likes', default=0)

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def get_url(self):
        return "/question/{}".format(self.id)


class Answer(models.Model):
    added_at = models.DateField(auto_now=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.SET(value='Deleted'))
    text = models.TextField(null=True)

    def __str__(self):
        return self.text

