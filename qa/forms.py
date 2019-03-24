from django.forms import ModelForm
from .models import Question, Answer

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset


class AskForm(ModelForm):
    """this is for creating new questions. Made it with ModelForm"""

    class Meta:
        """let's get field names from the model"""
        model = Question
        fields = ['title', 'text', 'author']
        exclude = ('author',)  # need to exclude this to pre-save form


class AnswerForm(ModelForm):
    """this is an answer form"""

    def __init__(self, *args, **kwargs):
        """here i am using the FormHelper class and its attributes to make the form look nicer"""

        super(AnswerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = "form-control"
        self.helper.form_id = 'id-answerForm'
        self.helper.layout = Layout(
            Fieldset('',  # the first param here is always a form label
                     'text')
        )
        self.helper.add_input(Submit('submit', 'Add Answer'))
        self.helper.form_show_labels = False  # don't want it to draw the actual model field name

    class Meta:
        model = Answer
        fields = ['text']
        exclude = ('author', 'question')
