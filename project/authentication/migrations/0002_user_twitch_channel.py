# Generated by Django 5.0.7 on 2024-07-16 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='twitch_channel',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
