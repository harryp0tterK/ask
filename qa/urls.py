from django.urls import path
from .views import home, question, ask, delete, edit, create_category, \
    serve_categories, QuestionLikeRedirect, QAnsweredRedirect


urlpatterns = [
    path('', home, name='home'),
    path('question/<int:qn_id>/', question, name='question'),
    path('question/<int:qn_id>/like/', QuestionLikeRedirect.as_view(), name='like'),
    path('answer/<int:a_id>/best/', QAnsweredRedirect.as_view(), name='best_answer'),
    path('question/', home),
    path('author/<int:a_id>/', home, name='author'),
    path('categories/', serve_categories, name='categories'),
    path('category/<int:a_id>', home, name='category'),
    path('create_category/', create_category, name='create_category'),
    path('popular/', home, name='popular'),
    path('ask/', ask, name='ask'),
    path('delete/<str:obj_type>/<int:o_id>', delete, name='delete'),
    path('edit/<str:obj_type>/<int:o_id>', edit, name='edit'),
]