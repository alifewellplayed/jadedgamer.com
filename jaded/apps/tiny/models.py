from django.db import models
from django.utils.translation import ugettext_lazy as _
from .managers import *


class Genre(models.Model):
    name = models.CharField(max_length=255)
    date_added = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    date_updated = models.DateTimeField(null=True, blank=True, auto_now=True)
    guid = models.CharField(max_length=32, unique=True)
    objects = GenreManager()

    class Meta:
        db_table = "tiny_genres"

    def __unicode__(self):
        return self.name


class Theme(models.Model):
    name = models.CharField(max_length=255)
    date_added = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    date_updated = models.DateTimeField(null=True, blank=True, auto_now=True)
    guid = models.CharField(max_length=32, unique=True)

    objects = ThemeManager()

    class Meta:
        db_table = "tiny_themes"

    def __unicode__(self):
        return self.name


class Concept(models.Model):
    name = models.CharField(max_length=255)
    date_added = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    date_updated = models.DateTimeField(null=True, blank=True, auto_now=True)
    guid = models.CharField(max_length=32, unique=True)

    class Meta:
        db_table = "tiny_concepts"

    def __unicode__(self):
        return self.name


class Franchise(models.Model):
    name = models.CharField(max_length=255)
    date_added = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    date_updated = models.DateTimeField(null=True, blank=True, auto_now=True)
    guid = models.CharField(max_length=32, unique=True)

    objects = UpdateManager()

    class Meta:
        db_table = "tiny_franchises"

    def __unicode__(self):
        return self.name


class Rating(models.Model):
    name = models.CharField(max_length=255)
    rating_board = models.CharField(max_length=255)
    date_added = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    date_updated = models.DateTimeField(null=True, blank=True, auto_now=True)
    guid = models.CharField(max_length=32, unique=True)

    objects = RatingManager()

    class Meta:
        db_table = "tiny_ratings"

    def __unicode__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=255)
    date_added = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    date_updated = models.DateTimeField(null=True, blank=True, auto_now=True)
    guid = models.CharField(max_length=32, unique=True)

    objects = RegionManager()

    class Meta:
        db_table = "tiny_regions"

    def __unicode__(self):
        return self.name


class Company(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    website = models.URLField(null=True, blank=True)
    founded = models.DateTimeField(null=True, blank=True)
    location_country = models.CharField(max_length=255, null=True, blank=True)
    location_state = models.CharField(max_length=255, null=True, blank=True)
    date_added = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    date_updated = models.DateTimeField(null=True, blank=True, auto_now=True)
    guid = models.CharField(max_length=32, unique=True)

    objects = UpdateManager()

    class Meta:
        db_table = "tiny_companies"
        verbose_name_plural = "Companies"

    def __unicode__(self):
        return self.name


class Platform(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=25, null=True, blank=True)
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.SET_NULL)
    original_price = models.IntegerField(null=True, blank=True)
    release_date = models.DateTimeField(null=True, blank=True)
    install_base = models.IntegerField(null=True, blank=True)
    online_support = models.BooleanField()
    date_added = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    date_updated = models.DateTimeField(null=True, blank=True, auto_now=True)
    guid = models.CharField(max_length=32, unique=True)

    objects = UpdateManager()

    class Meta:
        db_table = "tiny_platforms"

    def __unicode__(self):
        return self.name


class Game(models.Model):
    objects = NameManager()
    name = models.CharField(max_length=255, blank=True)
    rating = models.ManyToManyField(Rating, blank=True, verbose_name="Ratings")
    genres = models.ManyToManyField(Genre, blank=True, verbose_name="Genres used")
    themes = models.ManyToManyField(Theme, blank=True, verbose_name="Themes used")
    franchises = models.ManyToManyField(Franchise, blank=True, verbose_name="Franchises")
    developers = models.ManyToManyField(
        Company, related_name="developers", blank=True, verbose_name="Developers involved."
    )
    publishers = models.ManyToManyField(
        Company, related_name="publishers", blank=True, verbose_name="Companies involved."
    )
    platforms = models.ManyToManyField(Platform, blank=True, verbose_name="Platforms released to.")
    release_date = models.DateTimeField(null=True, blank=True)
    expected_release_month = models.CharField(max_length=255, null=True, blank=True)
    expected_release_year = models.CharField(max_length=255, null=True, blank=True)
    date_added = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    date_updated = models.DateTimeField(null=True, blank=True, auto_now=True)
    guid = models.CharField(max_length=32, unique=True, db_index=True)

    objects = UpdateManager()

    class Meta:
        db_table = "tiny_games"

    def __unicode__(self):
        return self.name


class Release(models.Model):
    name = models.CharField(max_length=255, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    release_date = models.DateTimeField(null=True, blank=True)
    expected_release_month = models.CharField(max_length=255, null=True, blank=True)
    expected_release_year = models.CharField(max_length=255, null=True, blank=True)
    region = models.ForeignKey(Region, null=True, blank=True, on_delete=models.SET_NULL)
    game_rating = models.ForeignKey(Rating, blank=True, null=True, on_delete=models.SET_NULL)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    date_added = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    date_updated = models.DateTimeField(null=True, blank=True, auto_now=True)
    guid = models.CharField(max_length=32, unique=True, db_index=True)

    objects = ReleaseManager()

    class Meta:
        db_table = "tiny_releases"

    def __unicode__(self):
        return self.name
