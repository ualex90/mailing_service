from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'main_app/index.html'
