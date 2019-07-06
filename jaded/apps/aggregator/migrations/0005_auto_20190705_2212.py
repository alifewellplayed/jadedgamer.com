# Generated by Django 2.1.3 on 2019-07-05 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0004_feedlist_feeds'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feedlistthrough',
            options={'ordering': ('-order',)},
        ),
        migrations.AddField(
            model_name='feed',
            name='feed_display',
            field=models.SmallIntegerField(choices=[(0, 'default'), (1, 'Display Thumbnails')], default=0),
        ),
    ]
