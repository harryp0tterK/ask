from django.contrib import admin
from .models import Answer, Question


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'added_at',)
    search_fields = ('author',)
    list_filter = ('author', 'added_at',)
    ordering = ('id',)


admin.site.register(Question, QuestionAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'added_at', 'question_id')


admin.site.register(Answer, AnswerAdmin)
