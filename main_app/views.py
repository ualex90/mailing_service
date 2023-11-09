from django.views.generic import TemplateView

from blog_app.models import Post
from main_app.utils import get_random_list


class IndexView(TemplateView):
    template_name = 'main_app/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['post_list'] = get_random_list(Post)
