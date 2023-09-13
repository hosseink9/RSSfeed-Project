import re
from .models import Podcast, Episode, Category, Generator, Image
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
            values_item = re.findall(pattern,str(rss_excluded_episodes))
            values_item = list(set(values_item))
            podcast.__setattr__(tag.replace(":","_"),values_item[0]) if len(values_item) == 1 else podcast.__setattr__(tag.replace(":","_"),values_item) 
        return podcast
    
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
        pod = self.get_podcast_data()

        author = PodcastAuthor.objects.create(name=pod.itunes_author)        
        category = Category.objects.create(name=pod.itunes_category)
        generator = Generator.objects.create(name=pod.generator)
        image = Image.objects.create(url=pod.url)

        podcast_object = Podcast.objects.create(
            title = pod.title,
            language = pod.language,
            itunes_type = pod.itunes_type,
            copy_right = pod.copyright,
            explicit = pod.itunes_explicit,
            description = pod.description,
            pubDate = pod.pubDate,
            last_build_date = pod.lastBuildDate,
            link = pod.link,
            itunes_subtitle = None if not pod.hasattr("itunes_subtitle") else pod.itunes_subtitle,
            itunes_keywords = None if not pod.hasattr("itunes_keywords") else pod.itunes_keywords,
            category = category,
            generator = generator,
            author = author,
            image = image
        )
        self.podcast_obj = podcast_object
        return podcast_object
    
    def save_episode_in_db(self):
        #--save episode--#
        episodes = self.get_episode_data()

        for episode in episodes:
            author = EpisodeAuthor.objects.create(name=episode.author)

            e = Episode.objects.create(
                title = episode.title,
                guid = episode.guid,
                itunes_duration = episode.itunes_duration,
                itunes_episode_type = episode.itunes_episodeType,
                itunes_explicit = episode.itunes_explicit,
                description = episode.description,
                enclosure = episode.enclosure,
                link = episode.link,
                pub_date = episode.pubDate,
                itunes_keywords = None if not episode.hasattr("itunes_keywords") else episode.itunes_keywords,
                itunes_player = None if not episode.hasattr("itunes_player") else episode.itunes_player,
                podcast = self.podcast_obj,
                episode_author = author
            )
            self.episodes_obj.append(e)
