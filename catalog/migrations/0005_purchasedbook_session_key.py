# Generated by Django 3.2.9 on 2022-05-14 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20220428_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchasedbook',
            name='session_key',
            field=models.CharField(default=None, max_length=128, null=True),
        ),
    ]
