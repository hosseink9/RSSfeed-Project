# Generated by Django 4.2.5 on 2023-10-12 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Generator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('hostname', models.CharField(blank=True, max_length=150, null=True)),
                ('genDate', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('url', models.CharField(blank=True, max_length=150, null=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('link', models.URLField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PodcastUrl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('url', models.URLField(unique=True)),
                ('title', models.CharField(max_length=150)),
                ('is_saved', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('language', models.CharField(max_length=50)),
                ('itunes_type', models.CharField(max_length=50)),
                ('copy_right', models.CharField(max_length=100)),
                ('explicit', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('pubDate', models.DateTimeField(blank=True, null=True)),
                ('last_build_date', models.DateTimeField(blank=True, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('itunes_subtitle', models.TextField(blank=True, null=True)),
                ('itunes_keywords', models.TextField(blank=True, null=True)),
                ('itunes_image', models.CharField(max_length=400)),
                ('category', models.ManyToManyField(to='podcast.category')),
                ('podcast_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='author.podcastauthor')),
                ('podcast_generator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='podcast.generator')),
                ('podcast_image', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='podcast.image')),
                ('podcast_url', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='podcast.podcasturl')),
            ],
        ),
    ]
