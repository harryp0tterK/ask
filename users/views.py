from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import CustomUser
from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class UpdateProfileView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):

    model = CustomUser
    fields = ('username', 'email', 'age', 'avatar')
    template_name = 'registration/update_profile.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('home')
    success_message = 'Success! You have updated your profile credentials!'

    def test_func(self):
        obj = self.get_object()
        return obj.id == self.request.user.id







