from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.urls import reverse
from django.contrib import messages
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .forms import CommentForm, SearchPosts
from django.db.models import Q
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

'''def home(request):
	context = {
		'posts' : Post.objects.all()
	}
	return render(request, 'blog/home.html', context)'''

class PostListView(ListView):
	model = Post
	template_name = "blog/home.html"
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5

	def get_queryset(self):
		filter_content = self.request.GET.get('content', '')
		filter_user = self.request.GET.get('search_by_user', None)
		new_context = Post.objects.filter(Q(title__icontains=filter_content) | Q(content__icontains=filter_content)).order_by('-date_posted')
		if (filter_user):
			new_context = new_context.filter(author = filter_user)
		return new_context
		 
	def get_context_data(self, **kwargs):
		context = super(PostListView, self).get_context_data(**kwargs)
		context['form'] = SearchPosts(self.request.GET)
		return context

class UserPostListView(ListView):
	model = Post
	template_name = "blog/user_posts.html"
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5

	def get_queryset(self):
		'''sovrascrivere la query? indagare '''
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
	model = Post
	def post(self, request, *args, **kwargs):
		form = CommentForm(request.POST)
		if form.is_valid():
			post = self.get_object()
			newcomment = Comment(content = form.data['message'], author=request.user, post=post)
			newcomment.save()
			messages.success(request, f'Commento aggiunto correttamente!')
			return redirect(reverse('post-detail', kwargs={"pk": post.id}))

	def get_context_data(self, **kwargs):
		post = self.get_object()
		context = super(PostDetailView, self).get_context_data(**kwargs)
		context['form_comments'] = CommentForm()
		return context

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']
	def form_valid(self, form):
		'''override del metodo di validazione'''
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']
	def form_valid(self, form):
		'''override del metodo di validazione'''
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		'''senza questa funzione non avviene il controllo'''
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

def about(request):
	return render(request, 'blog/about.html', { 'title' : 'About'})

#@login_required(login_url="login")