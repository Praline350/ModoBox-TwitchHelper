# Generated by Django 5.0.7 on 2024-07-27 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chatmessage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chatmessage',
            options={'ordering': ['-timestamp']},
        ),
    ]