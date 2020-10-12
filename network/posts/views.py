from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.edit import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from . models import Post
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
import json

# Create your views here.

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/home.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(comment_to=None).order_by('-date_posted')

class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self):
        context = super().get_context_data()
        context['profile'] = get_object_or_404(User, username=self.kwargs['username']).profile
        return context
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        return Post.objects.filter(author=user, comment_to=None).order_by('-date_posted')


class PostDetailView(LoginRequiredMixin, CreateView, SingleObjectMixin):
    model = Post
    template_name='posts/detail.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        post = Post.objects.get(pk=self.kwargs['pk'])
        form.instance.comment_to = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_object()
        paginator = Paginator(self.get_object().comments.order_by('-date_posted'), 10)
        page_obj = paginator.get_page(self.request.GET.get('page'))
        context['page_obj'] = page_obj
        return context

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.get_object().pk})


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'posts/create_post.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name= 'posts/update_post.html'
    fields = ['title', 'content']

    def test_func(self):
        if self.get_object().author == self.request.user:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    def test_func(self):
        if self.get_object().author == self.request.user:
            return True
        return False

    def get_success_url(self):
        if self.get_object().comment_to:
            return reverse('post-detail', kwargs={'pk': self.get_object().comment_to.pk})
        return '/'
    
class FollowingPostView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/following_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        following = self.request.user.profile.following.all()
        return Post.objects.filter(author__profile__in=following).order_by('-date_posted')

@login_required
def handleToggleLike(request):
    data = json.loads(request.body.decode('utf-8'))
    if data and data['post_id']:
        post = Post.objects.filter(pk=data['post_id']).first()
        if post is not None:
            if request.user in post.likes.all():
                post.likes.remove(request.user)
                liked = False
            else: 
                post.likes.add(request.user)
                liked = True
            return JsonResponse({
                'success': True,
                'res' : {
                    'liked': liked,
                    'number_likes': post.likes.count()
                }
            })
    return JsonResponse({'success': True,'alert': 'inappropriate input'})

@login_required
def handleToggleFollow(request):
    data = json.loads(request.body.decode('utf-8'))
    if data and data['username']:
        profile = User.objects.filter(username=data['username']).first().profile
        c_profile = request.user.profile
        if profile is not None and profile != c_profile:
            if c_profile in profile.followers.all():
                profile.followers.remove(c_profile)
                following = False
            else :
                profile.followers.add(c_profile)
                following = True
            return JsonResponse({
                'success': True,
                'res': {
                    'following': following,
                    'followers': profile.followers.count()
                }
            })
    return JsonResponse({'success': False})