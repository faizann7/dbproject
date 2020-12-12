# Generated by Django 3.0.8 on 2020-08-08 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20200807_2208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='watchlist',
        ),
        migrations.AddField(
            model_name='listings',
            name='created_by',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='listings',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('watchlist', models.ManyToManyField(blank=True, to='auctions.Listings')),
            ],
        ),
    ]