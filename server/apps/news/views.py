from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from .models import NewsItem, NewsItemInstance

class NewsList(ListView):
    template_name = 'news/news_list.html'

    def get_queryset(self):
        if self.kwargs['ordering']:
            self.news = get_object_or_404(NewsItem, name=self.kwargs['ordering'])
        else:
            return NewsItem.objects.public()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
