# Generated by Django 5.0.4 on 2024-07-02 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0003_rename_timestamp_friend_time_invitation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='status',
            field=models.CharField(choices=[('Waiting', 'Waiting'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='Waiting', max_length=10),
        ),
    ]
