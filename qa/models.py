from django.db import models
from users.models import CustomUser


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-added_at')

    def popular(self):
        return self.order_by('-rating')


# class Category(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.CharField(max_length=255, null=True, blank=True)
#
#     def __str__(self):
#         return self.name


class Question(models.Model):
    title = models.CharField(blank=False, null=False, max_length=255)
    text = models.TextField()
    added_at = models.DateField(auto_now=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(CustomUser, on_delete=models.SET(value='Deleted'))
    likes = models.ManyToManyField(CustomUser, related_name='get_likes', default=0)

    # category = models.ManyToManyField(Category)  # fixme here is the thing to start w/
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

