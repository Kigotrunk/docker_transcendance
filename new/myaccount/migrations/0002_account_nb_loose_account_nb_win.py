# Generated by Django 5.0.4 on 2024-06-27 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myaccount', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='nb_loose',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='account',
            name='nb_win',
            field=models.IntegerField(default=0),
        ),
    ]
