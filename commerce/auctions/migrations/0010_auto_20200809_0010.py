# Generated by Django 3.0.8 on 2020-08-08 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20200808_1952'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='watchlist',
            field=models.BooleanField(null=True),
        ),
        migrations.DeleteModel(
            name='WatchList',
        ),
    ]
