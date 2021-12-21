from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# Create your views here.


class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'post_lists'

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailVies(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post_details'


class PostCreateView(CreateView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post
    template_name = 'post_form.html'


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post
    template_name = 'post_form.html'


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
    context_object_name = 'post_deletes'
    template_name = 'post_confirm_delete.html'


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post
    context_object_name = 'draft_lists'
    template_name = 'draft_list.html'

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')

#####################################################################
#####################################################################


@login_required
def post_publish_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=post.pk)


@login_required
def add_comment_to_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def approve_comment_view(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def delete_comment_view(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)
