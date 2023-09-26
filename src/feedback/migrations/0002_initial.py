# Generated by Django 4.2.5 on 2023-09-26 12:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('feedback', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('podcast', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('episode', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='playlist',
            name='episodes',
            field=models.ManyToManyField(to='episode.episode'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='podcasts',
            field=models.ManyToManyField(to='podcast.podcast'),
        ),
        migrations.AddField(
            model_name='like',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='like',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='comment',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
    ]
