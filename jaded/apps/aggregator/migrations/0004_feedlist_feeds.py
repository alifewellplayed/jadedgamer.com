# Generated by Django 2.1.3 on 2019-07-05 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aggregator", "0003_auto_20190705_2043"),
    ]

    operations = [
        migrations.AddField(
            model_name="feedlist",
            name="feeds",
            field=models.ManyToManyField(blank=True, through="aggregator.FeedListThrough", to="aggregator.Feed"),
        ),
    ]
