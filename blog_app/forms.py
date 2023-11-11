from django import forms

from blog_app.models import Post
from service_app.forms import StyleFrmMixin


class PostForm(StyleFrmMixin, forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'body', 'image', 'is_published']
