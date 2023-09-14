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
