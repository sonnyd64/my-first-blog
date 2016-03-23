from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
import datetime

def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			if 'publish' in request.POST:
				post.publish()
			post.last_edit = timezone.now()
			post.save()
			if 'save' in request.POST:
				return redirect('post_edit', pk=post.pk)
			elif 'publish' in request.POST:
				return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			if 'publish' in request.POST:
				if post.published_date == None:
					post.publish()
			post.last_edit = timezone.now()
			post.save()
			if 'save' in request.POST:
				return render(request, 'blog/post_edit.html', {'form': form})
			elif 'publish' in request.POST:
				return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form})
