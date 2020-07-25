from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, path
from django.http import HttpResponseRedirect
from django.forms import model_to_dict

from .models import BlockedIp, LinkClick


@admin.register(BlockedIp)
class BlockedIpAdmin(admin.ModelAdmin):
    fields = ("name", "ip_addr")
    list_display = ["name", "ip_addr"]


@admin.register(LinkClick)
class LinkClickAdmin(admin.ModelAdmin):
    fields = ("user", "link", "referer", "user_agent", "ip_addr", "pub_date")
    list_display = ["user", "link", "referer"]
