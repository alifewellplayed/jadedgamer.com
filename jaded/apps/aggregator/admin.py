from django.contrib import admin

from .models import Feed, FeedItem, FeedList

def mark_approved(modeladmin, request, queryset):
    for item in queryset.iterator():
        item.approval_status = 3 #approved = 3
        item.save()

mark_approved.short_description = "Mark selected feeds as approved."

def mark_denied(modeladmin, request, queryset):
    for item in queryset.iterator():
        item.approval_status = 2 #denied = 2
        item.save()


admin.site.register(
    Feed,
    list_display=["title", "feed_type", "site_url", "approval_status"],
    list_filter=["feed_type", "approval_status"],
    ordering=["title"],
    search_fields=["title", "site_url"],
    raw_id_fields=['owner'],
    list_editable=["approval_status"],
    list_per_page=500,
    actions=[mark_approved, mark_denied],
)

admin.site.register(
    FeedItem,
    list_display=['title', 'feed', 'date_updated'],
    list_filter=['feed'],
    search_fields=['feed__title', 'feed__site_url', 'title'],
    date_heirarchy=['date_updated'],
)

admin.site.register(
    FeedList,
    prepopulated_fields={'slug': ('title',)},
)
