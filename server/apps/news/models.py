
from django.db import models
from django.core.cache import cache
from django.template.defaultfilters import slugify, striptags
from django.conf import settings
from django.template.defaultfilters import slugify

from .managers import NewsItemManager

class NewsItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField(blank=True, max_length=510)
    title = models.CharField(max_length=510)
    slug = models.SlugField(unique_for_date='timestamp', max_length=510)
    note = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="newsItems", verbose_name='user')
    date_added = models.DateTimeField(verbose_name="When list was added to the site", auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_hidden = models.BooleanField(default=False)
    objects = NewsItemManager()

    def all_tags(self, min_count=False):
        return Tag.objects.usage_for_model(NewsItemInstance, counts=False, min_count=None, filters={'newsitem': self.id})

    def all_tags_with_counts(self, min_count=False):
        return Tag.objects.usage_for_model(NewsItemInstance, counts=True, min_count=None, filters={'newsitem': self.id})=

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/id/%s/" % (self.id)

	def save(self, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		super(NewsItem, self).save(**kwargs)

    class Meta:
        ordering = ('-timestamp',)
        db_table = 'news_item'


class NewsItemInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    newsitem = models.ForeignKey(NewsItem, related_name="saved_instances", verbose_name='News')
    title = models.CharField(max_length=510)
    slug = models.SlugField(max_length=510)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="saved_news", verbose_name=_('user'))
    date_added = models.DateTimeField(verbose_name="When list was added to the site", auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    note = models.TextField(blank=True)

    def _create_news_item(self):
        news_item = NewsItem(url=self.url, title=self.title, slug=self.slug, note=self.note, user=self.user)
        news_item.save()
        return news_item

    def save(self, force_insert=False, force_update=False):
        if not self.id:
            self.slug = slugify(self.title)

        if self.url:
            try:
                news_item = NewsItem.objects.get(url=self.url)
            except NewsItem.DoesNotExist:
                news_item = self._create_news_item()
        else:
            news_item = self._create_news_item()

        self.news_item = news_item
        super(NewsItemInstance, self).save(force_insert, force_update)

    def delete(self):
        news_item = self.news_item
        super(NewsItemInstance, self).delete()
        if news_item.saved_instances.all().count() == 0:
            news_item.delete()

    def __str__(self):
        return "%(news_item)s for %(user)s" % {'news_item':self.news_item, 'user':self.user}

    class Meta:
        db_table = 'news_item_instance'
