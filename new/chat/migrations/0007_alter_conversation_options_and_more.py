# Generated by Django 5.0.4 on 2024-06-26 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_alter_conversation_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='conversation',
            options={'ordering': ['-last_message_sent_at', '-time']},
        ),
        migrations.AddField(
            model_name='conversation',
            name='last_message_sent_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]