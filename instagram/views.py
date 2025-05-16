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
from profiles.models import UserProfile, Follow
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from posts.models import Post
from django.urls import reverse
from django.views.generic import ListView
from profiles.forms import ProfileFollow

# Create your views here.

class HomeView(TemplateView):
    template_name = 'general/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Si el usuario está logueado
        if self.request.user.is_authenticated:
            # Obtenemos post de los usuarios que seguimos
            following = Follow.objects.filter(follower=self.request.user.profile).values_list('following__user', flat=True)
            # Nos traemos los posts de los usuarios que seguimos
            last_posts = Post.objects.filter(user__profile__user__in=following)
        else:
            # Si no está logueado, mostramos los últimos posts
            last_posts = Post.objects.all().order_by('-created_at')
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
class ProfileDetailView(DetailView, FormView):
    model = UserProfile
    template_name = 'general/profile_detail.html'
    context_object_name = 'profile'
    form_class = ProfileFollow

    def get_initial(self):
        self.initial['profile_pk'] = self.get_object().pk
        return super().get_initial()
    

    def form_valid(self, form):
        profile_pk = form.cleaned_data.get('profile_pk')
        action = form.cleaned_data.get('action')
        following = UserProfile.objects.get(pk=profile_pk)

        if Follow.objects.filter(
            follower=self.request.user.profile,
            following=following
        ).exists():
            Follow.objects.filter(
                follower=self.request.user.profile,
                following=following
            ).delete()
            messages.add_message(self.request, messages.SUCCESS, f'Usuario dejado de seguir correctamente.')
        else:
            Follow.objects.get_or_create(
                follower=self.request.user.profile,
                following=following
            )
            messages.add_message(self.request, messages.SUCCESS, f'Usuario seguido correctamente.')


        # if action == 'follow':
        #     Follow.objects.get_or_create(
        #         follower=self.request.user.profile,
        #         following=following
        #     )
        #     messages.add_message(self.request, messages.SUCCESS, f'Usuario seguido correctamente.')
        # elif action == 'unfollow':
       
        #     messages.add_message(self.request, messages.SUCCESS, f'Usuario dejado de seguir correctamente.')
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('profile_detail', args=[self.get_object().pk])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Comprobamos si seguimos al usuario

        following = Follow.objects.filter(follower=self.request.user.profile, following=self.get_object()).exists()
        context['following'] = following
        return context



@method_decorator(login_required, name='dispatch')
class ProfileListView(ListView):
    model = UserProfile
    template_name = 'general/profile_list.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        return UserProfile.objects.all().order_by('user__username').exclude(user=self.request.user)

        
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

    def dispatch(self, request, *args, **kwargs):
        user_profile = self.get_object()
        if user_profile.user != self.request.user:
            return HttpResponseRedirect(reverse('home'))
        return super().dispatch(request, *args, **kwargs)

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


# @login_required
# def follow(request, user_to_follow_pk):
#     user = get_object_or_404(User, pk=user_to_follow_pk)
    

#     if request.user != user:
#         return HttpResponseForbidden()

#     if user.profile.follows.filter(pk=user.pk).exists():
#         return HttpResponseRedirect(reverse('profiles:profile', args={user.username}))
#     user_to_follow_pk.profile.follows.add(user.profile)    