from django.urls import path
from .views import home, question, ask, delete, edit


urlpatterns = [
    path('', home, name='home'),
    path('question/<int:qn_id>/', question, name='question'),
    # path('question/<int:qn_id>/delete/', delete_question, name='delete'),
    path('delete/<str:obj_type>/<int:o_id>', delete, name='delete'),
    path('edit/<str:obj_type>/<int:o_id>', edit, name='edit'),
    path('question/', home),
    path('popular/', home, name='popular'),
    path('ask/', ask, name='ask')
]