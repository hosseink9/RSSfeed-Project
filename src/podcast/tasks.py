from celery import shared_task, Task
from django.db.models import Max
import datetime as dt
from time import sleep
import logging

from .models import Podcast
from episode.models import Episode
from author.models import PodcastAuthor, EpisodeAuthor

logger = logging.getLogger('django-celery')


class RetryTask(Task):
    autoretry_for = (Exception, KeyError)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = 2



@shared_task(bind=True, base=RetryTask)
def author(self,episode_list):
    author_list = list()
    dict_list = dict()

    for episode in episode_list:
        author = dict_list.get(episode.get("itunes_author")) or EpisodeAuthor.objects.get_or_create(name=episode.get("itunes_author"))[0] if episode.get('itunes_author') else None
        dict_list[episode.get("itunes_author")] = author
        author_list.append(author)

    author_list = list(map(lambda author:author.id if author else None,author_list))
    return author_list


@shared_task(bind=True, base=RetryTask)
def save_episode(self,episode_list,author_list,podcast_id):
    res_list = list()
    for index, episode in enumerate(episode_list):
        episode_field = Episode(
            title = episode.get("title"),
            guid = episode.get("guid"),
            itunes_duration = episode.get("itunes_duration"),
            itunes_episode_type = episode.get("itunes_episodeType"),
            itunes_explicit = episode.get("itunes_explicit"),
            description = episode.get("description"),
            enclosure = episode.get('enclosure'),
            link = episode.get("link"),
            pubDate = dt.datetime.strptime(episode.get("pubDate").replace('GMT','+0000'), "%a, %d %b %Y %H:%M:%S %z"),
            itunes_keywords = episode.get("itunes_keywords",None),
            itunes_player = episode.get("itunes_player",None),
            episode_podcast = Podcast.objects.get(id=podcast_id),
            episode_author = EpisodeAuthor.objects.get(id=author_list[index]) if author_list[index] else None
        )
        res_list.append(episode_field)
    Episode.objects.bulk_create(res_list)




@shared_task(bind=True, base=RetryTask,)
def update_task(self,podcast,episodes):
        sleep(30)
        author = PodcastAuthor.objects.filter(name=podcast.get("itunes_author")).first()
        podcast_object = Podcast.objects.get(title = podcast.get("title"), link = podcast.get("link"))
        episode_objects_list = Episode.objects.filter(episode_podcast = podcast_object).values_list("guid",flat=True)



