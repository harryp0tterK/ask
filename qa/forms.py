from django.forms import ModelForm
from .models import Question, Answer


class AskForm(ModelForm):
    """this is for creating new questions. Made it with ModelForm"""

    class Meta:
        model = Question
        fields = ['title', 'text']
        exclude = ('author',)


class AnswerForm(ModelForm):
    """this is an answer form"""

    class Meta:
        model = Answer
        fields = ['text']
        exclude = ('author', 'question')
