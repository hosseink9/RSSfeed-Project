import re
import datetime as dt
from django.db.models import Max
import logging

from .models import Podcast,Category, Generator, Image, Owner
from author.models import PodcastAuthor, EpisodeAuthor
from episode.models import Episode

logger = logging.getLogger("django-celery")


class Parser:
    item_tag_pattern = re.compile("<item>((\n|.)*?)</item>")
    tag_pattern = re.compile("<([^\<\>\[\]\- ]*)(?:\s*(\S*)=\"([^\"]*?)\"[^\>\]\[]*)*>")
    key_value_pair_pattern = re.compile('([^ ]*?)=\"(.*?)\"')

    def __init__(self, rss_path=None, rss_file=None, save=False, podcast_url=None):
        self.url = podcast_url
        self.rss_path = rss_path
        self.rss_file = rss_file or self._read_rss_file()
        podcast_data = self.get_podcast_data()
        podcast_object = Podcast.objects.filter(title = podcast_data.get("title"),link= podcast_data.get("link"))
        self.podcast_object = podcast_object.get() if podcast_object else None
        self.episodes_obj = list()
        # self.save_podcast_in_db() if save is True else None
        # self.save_episode() if save is True else None
        if save:
            self.save_podcast_in_db() if not self.check_exist()[0] else None
            self.save_episode() if not self.check_exist()[1] else None

    def _read_rss_file(self):
        with open(self.rss_path, "rt", encoding="utf-8") as file:
            rss_file = file.read()
        return rss_file

    def get_podcast_data(self):
        rss_excluded_episodes = re.sub("<item>(?:.|\n)*?<\/item>","", self.rss_file)
        match_list = self.tag_pattern.finditer(rss_excluded_episodes)
        podcast_tags_name = list(set([item.group(1).replace('/', "") for item in match_list])) #/title -> title
        podcast = {}

        for tag in podcast_tags_name:
            pattern = f"(?:<{tag}.*?>)(.*?)(?:<\/{tag}>)"
            close_pattern = f"(?:<itunes:category+)(.*?)(?:/>)"
            category_set = re.findall(close_pattern, str(rss_excluded_episodes))

            close_pattern_image = f"(?:<itunes:image+)(.*?)(?:/>)"
            image_set = re.findall(close_pattern_image, str(rss_excluded_episodes))

            close_pattern_atom_link = f"(?:<atom:link+)(.*?)(?:/>)"
            atom_link_set = re.findall(close_pattern_atom_link, str(rss_excluded_episodes))

            key_value_pattern = '([^ ]*?)=\"(.*?)\"'
            category_value = re.findall(key_value_pattern, str(category_set))

            image_value = re.findall(key_value_pattern, str(image_set))

            atom_link_value = re.findall(key_value_pattern, str(atom_link_set))

            values_item = re.findall(pattern,str(rss_excluded_episodes))
            values_item = list(set(values_item))
            podcast[tag.replace(":","_")]="".join(values_item)
        podcast["itunes_category"] = category_value[0][1]
        podcast["itunes_image"] = image_value[0][1]
        podcast["atom_link"] = atom_link_value[0][1] if len(atom_link_value) >= 1 else None
        return podcast

    def check_exist(self):

        podcast_dict = self.get_podcast_data()
        old_podcast = Podcast.objects.filter(title=podcast_dict.get("title"), link=podcast_dict.get("link"))
        if old_podcast:
            if old_podcast.get().episode.all():
                return True,True
            return True,False
        return False,False

    def get_episode_data(self):
        podcast_dict = self.get_podcast_data()
        item_list = self.item_tag_pattern.findall(self.rss_file)
        episode_list = []

        for item in item_list:
            episode1 ={"podcast":podcast_dict}
            match_list = self.tag_pattern.finditer(item[0])
            episode_tags_name = list(set([item.group(1).replace('/', "") for item in match_list]))

            for tag in episode_tags_name:
                pattern = f'(?:<{tag}.*?>)(.*?)(?:<\/{tag}>)'
                values_item = re.findall(pattern,str(item))
                episode1[tag.replace(":","_")] = "".join(values_item)
            episode_list.append(episode1)

        return episode_list


    def save_podcast_in_db(self):
        #--save podcast--#
        assert self.check_exist()[0] == False, "Podcast already exist."
        pod = self.get_podcast_data()
        author = PodcastAuthor.objects.get_or_create(name=pod.get("itunes_author"))[0]
        category = Category.objects.get_or_create(name=pod.get("itunes_category"))[0]
        generator = Generator.objects.get_or_create(name=pod.get("generator"))[0] if pod.get("generator") else None
        image = Image.objects.get_or_create(url= pod.get("url",pod.get('itunes_image')))[0] if pod.get("url",pod.get('itunes_image')) else None
        owner = Owner.objects.get_or_create(name=pod.get("itunes_name"), email=pod.get("itunes_email"))[0]

        podcast_object = Podcast.objects.create(
            title = pod.get("title"),
            url = pod.get("atom_link"),
            language = pod.get("language"),
            itunes_type = pod.get("itunes_type"),
            copy_right = pod.get("copyright"),
            explicit = pod.get("itunes_explicit"),
            description = pod.get("description"),
            pubDate = dt.datetime.strptime(pod.get("pubDate"), "%a, %d %b %Y %H:%M:%S %z") if pod.get("pubDate") else None, #“Mon, 4 Sep 2023 07:00:00 +0000”
            last_build_date = dt.datetime.strptime(pod.get("lastBuildDate"), "%a, %d %b %Y %H:%M:%S %z") if pod.get("lastBuildDate") else None,
            link = pod.get("link"),
            itunes_subtitle = pod.get("itunes_subtitle",None) ,
            itunes_keywords = pod.get("itunes_keywords", None) ,
            itunes_image = pod.get("itunes_image"),
            # category = category,
            podcast_generator = generator,
            podcast_author = author,
            podcast_image = image,
            podcast_url = self.url
        )
        self.url.is_save = True
        self.url.save()
        podcast_object.category.add(category)
        podcast_object.save()
        self.podcast_object = podcast_object
        return podcast_object


    def save_episode(self):
        #--save episode--#
        assert self.check_exist()[1] == False, "Episodes already exist."
        episodes = self.get_episode_data()
        author_list = self.get_author_objects(episodes)

        self.save_episode_in_db(episodes, author_list, self.podcast_object)


    def get_author_objects(self,episode_list):
        author_list = list()
        dict_list = dict()

        for episode in episode_list:
            author = dict_list.get(episode.get("itunes_author")) or EpisodeAuthor.objects.get_or_create(name=episode.get("itunes_author"))[0] if episode.get('itunes_author') else None
            dict_list[episode.get("itunes_author")] = author
            author_list.append(author)

        author_list = list(map(lambda author:author.id if author else None,author_list))
        return author_list



    def save_episode_in_db(self,episode_list,author_list,podcast_object):
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
                episode_podcast = podcast_object, # Podcast.objects.get(id=podcast_id),
                episode_author = EpisodeAuthor.objects.get(id=author_list[index]) if author_list[index] else None
            )
            res_list.append(episode_field)
        Episode.objects.bulk_create(res_list)


    def update_exist_podcast(self):
        podcast = self.get_podcast_data()
        episodes = self.get_episode_data()
        podcast_object = Podcast.objects.get(title = podcast.get("title"), link = podcast.get("link"))
        episode_objects_list = Episode.objects.filter(episode_podcast = podcast_object).values_list("guid",flat=True)

        podcast_last_update = dt.datetime.strptime(podcast.get("pubDate"),"%a, %d %b %Y %H:%M:%S %z") if podcast.get("pubDate") else max(list(map(lambda item:dt.datetime.strptime(item.get("pubDate"),"%a, %d %b %Y %H:%M:%S %z"), episodes)))

        podcast_object_last_update = podcast_object.pubDate or Episode.objects.aggregate(Max("pubDate")).get("pubDate__max")


        if not podcast_object:
            return "This podcast didn't save in database"

        episode_update_list = []
        if podcast_object_last_update < podcast_last_update:
            for new_episode in episodes:
                if new_episode.get("guid") not in episode_objects_list:
                    episode_update_list.append(new_episode)
            author_list = self.get_author_objects(episode_update_list)

            self.save_episode_in_db(episode_update_list, author_list, podcast_object)
            return "Updated successfully"

        return "xml file has not new episode for update!!"