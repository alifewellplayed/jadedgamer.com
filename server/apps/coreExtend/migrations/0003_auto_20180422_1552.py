# Generated by Django 2.0 on 2018-04-22 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreExtend', '0002_auto_20170201_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
    ]
