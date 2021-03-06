# Generated by Django 3.0.8 on 2020-08-05 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20200729_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='username',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='listings',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
