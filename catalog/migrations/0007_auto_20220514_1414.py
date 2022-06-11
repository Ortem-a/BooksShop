# Generated by Django 3.2.9 on 2022-05-14 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_auto_20220514_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='favoriteauthor',
            name='session_key',
            field=models.CharField(default=None, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='favoriteauthor',
            name='user',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='favoriteauthor',
            name='author',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]