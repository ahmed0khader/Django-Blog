from django.shortcuts import render, get_object_or_404
from django.views.generic import( 
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView,
    )
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import *
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'pages/blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'pages/blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted'] 
    paginate_by = 10
    
# user

class UserPostListView(ListView):
    model = Post
    template_name = 'pages/blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post
    template_name = 'pages/blog/post_detail.html'

#لانشاء بوست جديد
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'pages/blog/post_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# للتعديل على البوست 
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'pages/blog/post_form.html'
    fields = ['title', 'content']

# ممنوع حدا ينشر الا الي مسجل دخول 
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# لمنع اي حدا يعدل غير صاحب المنشور 
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'pages/blog/post_confirm_delete.html.html'

    # لمنع اي حدا يعدل غير صاحب المنشور 
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    context = {
        'title' : 'About',

    }
    return render(request, 'pages/blog/about.html', context)
