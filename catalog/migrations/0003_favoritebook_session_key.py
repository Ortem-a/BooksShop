# Generated by Django 3.2.9 on 2022-04-28 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_buy_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='favoritebook',
            name='session_key',
            field=models.CharField(default=None, max_length=128, null=True),
        ),
    ]
