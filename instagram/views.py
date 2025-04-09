from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm
from django.contrib import messages
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect


# Create your views here.

class HomeView(TemplateView):
    template_name = 'general/home.html'


class LoginView(FormView):
    template_name = 'general/login.html'
    # model = User
    # success_url = reverse_lazy('home')
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, f'Bienvenido {user.username}')
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            messages.add_message(self.request, messages.ERROR, "Usuario o contraseña incorrecta.")
            return super(LoginView, self).form_invalid(form)


class RegisterView(CreateView):
    template_name = 'general/register.html'
    model = User
    success_url = reverse_lazy('login')
    form_class = RegistrationForm

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Usuario creado correctamente.")
        return super(RegisterView, self).form_valid(form)
  



class LegalView(TemplateView):
    template_name = 'general/legal.html'

class ContactView(TemplateView):
    template_name = 'general/contact.html'



def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, "Has cerrado sesión correctamente.")
    return HttpResponseRedirect(reverse_lazy('home'))


