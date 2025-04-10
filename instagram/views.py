from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm
from django.contrib import messages
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from profiles.models import UserProfile
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from posts.models import Post



# Create your views here.

class HomeView(TemplateView):
    template_name = 'general/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        last_posts = Post.objects.all().order_by('created_at')[:5]
        context['last_posts'] = last_posts

        return context

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


@method_decorator(login_required, name='dispatch')
class ProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'general/profile_detail.html'
    context_object_name = 'profile'


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    model = UserProfile
    template_name = "general/profile_update.html"
    context_object_name = "profile"
    fields = [
        'profile_picture',
        'bio',
        'birth_date',
    ]
    # success_url = reverse_lazy('')

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Perfil editado correctamente.")
        return super(ProfileUpdateView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('profile_detail', args=[self.object.pk])


@login_required
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, "Has cerrado sesión correctamente.")
    return HttpResponseRedirect(reverse_lazy('home'))


