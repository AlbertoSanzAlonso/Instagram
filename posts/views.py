from django.views.generic import CreateView
from posts.models import Post
from .forms import PostCreateForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    template_name = 'post/post_create.html'
    model = Post
    form_class = PostCreateForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.add_message(self.request, messages.SUCCESS, "Publicación creada correctamente")
        return super(PostCreateView,self).form_valid(form)
    