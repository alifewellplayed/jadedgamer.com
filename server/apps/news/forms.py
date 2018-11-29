from django import forms
from .models import NewsItemInstance

class NewsItemInstanceModelForm(forms.ModelForm):
    title = forms.CharField(
        max_length=250,
        widget=forms.TextInput(attrs={
            'class': 'required form-control',
            'placeholder': 'Post Title',
        }),
    )

    note = forms.CharField(
        max_length=250,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Optional Note',
        }),
    )

    url = forms.URLField(
        label='URL',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://',
        }),
    )

    class Meta:
        model = NewsItemInstance
        exclude = ('id', 'slug', 'user', 'newsitem', 'date_added', 'date_updated', 'is_hidden')

    def clean_url(self):
        url = self.cleaned_data.get('url')
        return url
