# Generated by Django 5.0.4 on 2024-07-28 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myaccount', '0007_merge_20240728_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='highest_score',
            field=models.IntegerField(default=0),
        ),
    ]
