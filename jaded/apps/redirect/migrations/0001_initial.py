# Generated by Django 2.2.3 on 2019-07-06 21:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("aggregator", "0006_auto_20190706_2020"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlockedIp",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(blank=True, max_length=128)),
                ("ip_addr", models.GenericIPAddressField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="LinkClick",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("referer", models.CharField(max_length=512)),
                ("user_agent", models.CharField(max_length=1024, null=True)),
                ("ip_addr", models.GenericIPAddressField()),
                ("pub_date", models.DateTimeField(auto_now_add=True)),
                (
                    "link",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="clicks",
                        to="aggregator.FeedItem",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={"ordering": ("-pub_date",), "unique_together": {("link", "ip_addr")},},
        ),
    ]
