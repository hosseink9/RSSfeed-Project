import re
import datetime as dt
from .models import Podcast,Category, Generator, Image, Owner
from episode.models import Episode
from author.models import EpisodeAuthor, PodcastAuthor

class PodcastModel:
    def __init__(self, xml=None):
        self.xml = xml

class EpisodeModel:
    def __init__(self,podcast, title=None,author=None,guid=None,description=None,pubDate=None,link=None,itunes_title=None) -> None:
        self.title=title
        self.author=author
        self.guid=guid
        self.description=description
        self.pubDate=pubDate
        self.link=link
        self.itunes_title=itunes_title

class Parser:
    item_tag_pattern = re.compile("<item>((\n|.)*?)</item>")
    tag_pattern = re.compile("<([^\<\> ]*)(?:\s*(\S*)=\"([^\"]*?)\"[^\>]*)*>")
    key_value_pair_pattern = re.compile('([^ ]*?)=\"(.*?)\"')

    def __init__(self, rss_path=None, rss_file=None, save=False):
        self.rss_path = rss_path
        self.rss_file = rss_file or self._read_rss_file()
        self.podcast_obj = None
        self.episodes_obj = list()
        self.save_podcast_in_db() if save is True else None
        self.save_episode_in_db() if save is True else None

    def _read_rss_file(self):
        with open(self.rss_path, "rt", encoding="utf-8") as file:
            rss_file = file.read()
        return rss_file

    def get_podcast_data(self):
        rss_excluded_episodes = re.sub("<item>(?:.|\n)*?<\/item>","", self.rss_file)
        match_list = self.tag_pattern.finditer(rss_excluded_episodes)
        podcast_tags_name = list(set([item.group(1).replace('/', "") for item in match_list])) #/title -> title
        podcast = PodcastModel()

        for tag in podcast_tags_name:
            pattern = f"(?:<{tag}.*?>)(.*?)(?:<\/{tag}>)"
            close_pattern = f"(?:<itunes:category+)(.*?)(?:/>)"
            category_set = re.findall(close_pattern, str(rss_excluded_episodes))
            key_value_pattern = '([^ ]*?)=\"(.*?)\"'
            category_value = re.findall(key_value_pattern, str(category_set))

            values_item = re.findall(pattern,str(rss_excluded_episodes))
            values_item = list(set(values_item))
            podcast.__setattr__(tag.replace(":","_"),values_item[0]) if len(values_item) == 1 else podcast.__setattr__(tag.replace(":","_"),values_item)
        podcast.itunes_category = category_value[0][1]
        return podcast

    def check_exist(self):
        py_model = self.get_podcast_data()
        episode_model = self.get_episode_data()
        old_author = PodcastAuthor.objects.filter(name=py_model.itunes_author)
        if old_author:
            old_podcast = Podcast.objects.filter(title=py_model.title, link=py_model.link, author=old_author.first())
            if old_podcast:
                old_episode = Episode.objects.filter(guid = episode_model[0].guid)
                if old_episode:
                    return True
        return False

    def get_episode_data(self):
        podcast_obj = self.get_podcast_data()
        item_list = self.item_tag_pattern.findall(self.rss_file)
        episode_list = []

        for item in item_list:
            episode1 = EpisodeModel(podcast=podcast_obj)
            match_list = self.tag_pattern.finditer(item[0])
            episode_tags_name = list(set([item.group(1).replace('/', "") for item in match_list]))

            for i in episode_tags_name:
                pattern = f'(?:<{i}.*?>)(.*?)(?:<\/{i}>)'
                values_item = re.findall(pattern,str(item))
                episode1.__setattr__(i.replace(":","_"),values_item[0]) if len(values_item) == 1 else episode1.__setattr__(i.replace(":","_"),values_item)
            episode_list.append(episode1)

        return episode_list

    def save_podcast_in_db(self):
        #--save podcast--#
        assert self.check_exist() == False, "Podcast already exist."
        pod = self.get_podcast_data()
        author = PodcastAuthor.objects.create(name=pod.itunes_author)
        category = Category.objects.create(name=pod.itunes_category)
        generator = Generator.objects.create(name=pod.generator)
        image = Image.objects.create(url=pod.url)
        owner = Owner.objects.create(name=pod.itunes_name, email=pod.itunes_email)

        podcast_object = Podcast.objects.create(
            title = pod.title,
            language = pod.language,
            itunes_type = pod.itunes_type,
            copy_right = pod.copyright,
            explicit = pod.itunes_explicit,
            description = pod.description,
            pubDate = dt.datetime.strptime(pod.pubDate, "%a, %d %b %Y %H:%M:%S %z") if hasattr(pod,'pubDate') else None, #“Mon, 4 Sep 2023 07:00:00 +0000”
            last_build_date = dt.datetime.strptime(pod.lastBuildDate, "%a, %d %b %Y %H:%M:%S %z") if hasattr(pod,'last_build_date') else None,
            link = pod.link,
            itunes_subtitle = pod.itunes_subtitle if hasattr(pod, "itunes_subtitle") else None ,
            itunes_keywords = pod.itunes_keywords if hasattr(pod, "itunes_keywords") else None,
            # category = category,
            podcast_generator = generator,
            podcast_author = author,
            podcast_image = image
        )
        podcast_object.category.add(category)
        podcast_object.save()
        self.podcast_obj = podcast_object
        return podcast_object

    def save_episode_in_db(self):
        #--save episode--#
        assert self.check_exist() == False, "Episodes already exist."
        episodes = self.get_episode_data()
        res_list = list()
        author_list = list()
        dict_list = dict()

        for i in episodes:
            author = dict_list.get(i.author) or EpisodeAuthor(name=i.author) #content@audiochuck.com (audiochuck) -> (audiochuck)content@audiochuck.com
            dict_list[i.author] = author
            author_list.append(author)

        uniq_list = dict_list.values()
        EpisodeAuthor.objects.bulk_create(uniq_list)

        for index, episode in enumerate(episodes):
            episode_field = Episode(
                title = episode.title,
                guid = episode.guid,
                itunes_duration = episode.itunes_duration,
                itunes_episode_type = episode.itunes_episodeType,
                itunes_explicit = episode.itunes_explicit,
                description = episode.description,
                enclosure = episode.enclosure,
                link = episode.link,
                pubDate = dt.datetime.strptime(episode.pubDate, "%a, %d %b %Y %H:%M:%S %z"),
                itunes_keywords = None if not hasattr(episode, "itunes_keywords") else episode.itunes_keywords,
                itunes_player = None if not hasattr(episode, "itunes_player") else episode.itunes_player,
                episode_podcast = self.podcast_obj,
                episode_author = author_list[index]
            )
            res_list.append(episode_field)
            # self.episodes_obj.append(e)
        Episode.objects.bulk_create(res_list)
