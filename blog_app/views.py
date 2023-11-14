from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from pytils.translit import slugify

from blog_app.forms import PostForm
from blog_app.models import Post


class PostListView(ListView):
    model = Post
    paginate_by = 5
    queryset = Post.objects.filter().order_by('pk').reverse()
    extra_context = {
        'title': 'Блог',
        'description': 'Наши события'
    }


class PostEditListView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 10
    queryset = Post.objects.filter().order_by('pk')
    template_name = 'blog_app/post_edit_list.html'
    extra_context = {
        'title': 'Управление',
        'description': 'Настройка ленты'
    }


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        self.objects = super().get_object(queryset)
        self.objects.views_count += 1
        self.objects.save()
        return self.objects

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        post_item = Post.objects.get(pk=self.kwargs.get('pk'))
        context_data['title'] = post_item.slug
        context_data['description'] = post_item.title

        return context_data


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    permission_required = 'blog_app.add_post'
    form_class = PostForm
    extra_context = {
        'title': 'Новая запись',
        'description': 'Создание новой записи в блог'
    }

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.title)
            new_post.owner = self.request.user
            new_post.save()
        return super().form_valid(form)

    def get_success_url(self):
        # return reverse('blog_app:blog_app', args=[self.object.pk])
        return reverse('blog_app:edit_list')


class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Post
    permission_required = 'blog_app.change_post'
    form_class = PostForm
    extra_context = {
        'title': 'Новая запись',
        'description': 'Создание новой записи в блог'
    }

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.title)
            new_post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog_app:post', args=[self.object.pk])


class PostDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Post
    permission_required = 'blog_app.delete_post'
    extra_context = {
        'title': 'Удаление',
        'description': 'Удаление записи',
    }

    def get_success_url(self):
        return reverse('blog_app:blog')


def published(request, pk):
    post_item = get_object_or_404(Post, pk=pk)
    if post_item.is_published:
        post_item.is_published = False
    else:
        post_item.is_published = True

    post_item.save()

    return redirect(reverse('blog_app:edit_list'))

