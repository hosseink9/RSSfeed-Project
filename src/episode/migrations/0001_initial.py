# Generated by Django 4.2.4 on 2023-09-27 22:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('podcast', '0001_initial'),
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('guid', models.CharField(max_length=50)),
                ('itunes_duration', models.CharField(max_length=50)),
                ('itunes_episode_type', models.CharField(max_length=50)),
                ('itunes_explicit', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField()),
                ('enclosure', models.CharField(blank=True, max_length=100, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('pubDate', models.DateTimeField(blank=True, null=True)),
                ('itunes_keywords', models.TextField(blank=True, null=True)),
                ('itunes_player', models.CharField(blank=True, max_length=100, null=True)),
                ('episode_author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='author.episodeauthor')),
                ('episode_podcast', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episode', to='podcast.podcast')),
            ],
        ),
    ]
