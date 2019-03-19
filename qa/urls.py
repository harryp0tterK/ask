from django.urls import path
from .views import home, question, ask


urlpatterns = [
    path('', home, name='home'),
    path('question/<int:qn_id>/', question, name='question'),
    path('popular/', home, name='popular'),
    path('ask/', ask, name='ask')
]