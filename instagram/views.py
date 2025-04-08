from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import RegistrationForm


# Create your views here.

class HomeView(TemplateView):
    template_name = 'general/home.html'


class LoginView(TemplateView):
    template_name = 'general/login.html'


class RegisterView(CreateView):
    model = User
    template_name = 'general/register.html'
    # fields = ['first_name', 'username', 'email', 'password']
    form_class = RegistrationForm
    success_url = reverse_lazy('home')



class LegalView(TemplateView):
    template_name = 'general/legal.html'

class ContactView(TemplateView):
    template_name = 'general/contact.html'







