# Generated by Django 5.0.4 on 2024-07-03 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myaccount', '0002_account_nb_loose_account_nb_win'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_connected',
            field=models.BooleanField(default=False),
        ),
    ]
