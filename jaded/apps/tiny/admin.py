from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import Genre, Theme, Franchise, Rating, Region, Company, Platform, Game, Release


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "date_added",
        "date_updated",
    )


class ThemeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "date_added",
        "date_updated",
    )


class FranchiseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "date_added",
        "date_updated",
    )


class RatingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "rating_board",
        "date_added",
        "date_updated",
    )
    list_filter = ("rating_board",)


class RegionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "date_added",
        "date_updated",
    )


class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "founded",
        "location_country",
        "date_added",
        "date_updated",
    )


class PlatformAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "abbreviation",
        "original_price",
        "company",
        "release_date",
        "install_base",
        "online_support",
    )
    list_filter = ("online_support",)


class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "release_date", "expected_release_year", "date_updated")
    list_filter = (
        "release_date",
        "platforms",
    )


class ReleaseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "game", "release_date", "expected_release_year", "platform", "region")
    list_filter = (
        "release_date",
        "region",
        "platform",
    )


admin.site.register(Genre, GenreAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Franchise, FranchiseAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Release, ReleaseAdmin)
