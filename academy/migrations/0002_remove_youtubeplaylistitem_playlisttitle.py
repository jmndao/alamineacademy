# Generated by Django 3.0.7 on 2020-09-24 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='youtubeplaylistitem',
            name='playlistTitle',
        ),
    ]
