from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import NewsItem, NewsItemInstance
from .forms import NewsItemInstanceModelForm

class NewsList(ListView):
    template_name = 'news/news_list.html'

    def get_queryset(self):
        return NewsItem.objects.public()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def AddNews(request):
    #Lets users add new feeds to the aggregator.
    instance = NewsItemInstance(user=request.user)
    f = NewsItemInstanceModelForm(request.POST or None, instance=instance)
    if f.is_valid():
        f.save()
        messages.add_message(
            request, messages.INFO, 'News item added.')
        return redirect('aggregator:Index')

    ctx = {'form': f, 'adding': True}
    return render(request, 'news/edit-news.html', ctx)
