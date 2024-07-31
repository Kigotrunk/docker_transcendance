# Generated by Django 5.0.4 on 2024-06-20 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('game', '0004_delete_ball_delete_pad'),
    ]

    operations = [
        migrations.CreateModel(
            name='partie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player1', models.CharField(max_length=100)),
                ('player2', models.CharField(max_length=100)),
                ('score_player1', models.IntegerField()),
                ('score_player2', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Game',
                'verbose_name_plural': 'Games',
            },
        ),
    ]