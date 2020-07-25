from django import forms
from .models import Feed


class FeedModelForm(forms.ModelForm):
    title = forms.CharField(
        max_length=250,
        widget=forms.TextInput(attrs={"class": "required form-control", "placeholder": "Website name",}),
    )
    feed_url = forms.URLField(
        label="Feed URL",
        help_text="Only RSS is currently supported. Other formats coming soon.",
        widget=forms.TextInput(attrs={"class": "required form-control", "placeholder": "Link to the RSS/Atom feed",}),
    )
    site_url = forms.URLField(
        label="Public URL",
        widget=forms.TextInput(
            attrs={"class": "required form-control", "placeholder": "Link to main page (i.e. blog homepage)",}
        ),
    )

    class Meta:
        model = Feed
        exclude = (
            "id",
            "feed_type",
            "slug",
            "owner",
            "approval_status",
            "active",
            "feed_list",
            "next_scheduled_update",
            "last_story_date",
            "subscribers",
            "num_subscribers",
            "has_feed_exception",
            "favicon_color",
            "favicon_not_found",
            "search_indexed",
            "pubsub_enabled",
            "has_page_exception",
            "tags",
            "date_added",
            "date_updated",
        )

    def clean_feed_url(self):
        feed_url = self.cleaned_data.get("feed_url")
        return feed_url
