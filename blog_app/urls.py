from django.urls import path

from blog_app.apps import BlogAppConfig
from blog_app.views import PostCreateView, PostEditListView, PostListView, PostUpdateView, PostDetailView, \
    PostDeleteView, published

app_name = BlogAppConfig.name

urlpatterns = [
    path('', PostListView.as_view(), name='blog'),
    path('edit_list/', PostEditListView.as_view(), name='edit_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post'),
    path('create/', PostCreateView.as_view(), name='create'),
    path('update/<int:pk>/', PostUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='delete'),
    path('published/<int:pk>/', published, name='published'),
]
