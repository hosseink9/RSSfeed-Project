# Generated by Django 4.2.5 on 2023-10-25 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0002_alter_image_url'),
        ('episode', '0002_alter_episode_enclosure_alter_episode_guid'),
        ('feedback', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='episodes',
            field=models.ManyToManyField(blank=True, null=True, to='episode.episode'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='podcasts',
            field=models.ManyToManyField(blank=True, null=True, to='podcast.podcast'),
        ),
    ]
