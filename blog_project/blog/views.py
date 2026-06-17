
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required

from .add_comment import can_comment
from .models import Post, Comment
from .forms import CommentForm

@cache_page(300)
def post_list(request):
    posts = Post.objects.select_related('author')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(
        Post.objects.select_related('author').prefetch_related('comments__author'),
        pk=pk
    )
    comments = post.comments.all()

    form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if not can_comment(request.user):

        return redirect('post_detail', pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

    return redirect('post_detail', pk=pk)


