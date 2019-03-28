from django.urls import path
from .views import home, question, ask, delete, edit


urlpatterns = [
    path('', home, name='home'),
    path('question/<int:qn_id>/', question, name='question'),
    path('question/', home),
    path('author/<int:a_id>/', home, name='author'),
    path('popular/', home, name='popular'),
    path('ask/', ask, name='ask'),
    path('delete/<str:obj_type>/<int:o_id>', delete, name='delete'),
    path('edit/<str:obj_type>/<int:o_id>', edit, name='edit'),

]