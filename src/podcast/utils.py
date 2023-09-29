import re
import datetime as dt
from .models import Podcast,Category, Generator, Image, Owner
from author.models import PodcastAuthor
from .tasks import update_task, save_episode, author


class Parser:
    item_tag_pattern = re.compile("<item>((\n|.)*?)</item>")
    tag_pattern = re.compile("<([^\<\>\[\]\- ]*)(?:\s*(\S*)=\"([^\"]*?)\"[^\>\]\[]*)*>")
    key_value_pair_pattern = re.compile('([^ ]*?)=\"(.*?)\"')

    def __init__(self, rss_path=None, rss_file=None, save=False):
        self.rss_path = rss_path
        self.rss_file = rss_file or self._read_rss_file()
        podcast_data = self.get_podcast_data()
        podcast_object = Podcast.objects.filter(title = podcast_data.get("title"),link= podcast_data.get("link"))
        self.podcast_object = podcast_object.get() if podcast_object else None
        self.episodes_obj = list()
        if save:
            self.save_podcast_in_db() if not self.check_exist()[0] else None
            self.save_episode_in_db() if not self.check_exist()[1] else None

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
        author = PodcastAuthor.objects.create(name=pod.get("itunes_author"))
        category = Category.objects.create(name=pod.get("itunes_category"))
        generator = Generator.objects.create(name=pod.get("generator")) if pod.get("generator") else None
        image = Image.objects.create(url= pod.get("url",pod.get('itunes_image'))) if pod.get("url",pod.get('itunes_image')) else None
        owner = Owner.objects.create(name=pod.get("itunes_name"), email=pod.get("itunes_email"))

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
            podcast_image = image
        )
        print(self.get_podcast_data())
        podcast_object.category.add(category)
        podcast_object.save()
        self.podcast_object = podcast_object
        return podcast_object

    def save_episode_in_db(self):
        #--save episode--#
        assert self.check_exist()[1] == False, "Episodes already exist."
        episodes = self.get_episode_data()
        author_list = author.delay(episodes).get()

        self.parse_episode(episodes, author_list, self.podcast_object)


    def update_exist_podcast(self):
        update = update_task.delay(self.get_podcast_data(),self.get_episode_data())
        return update


    def parse_episode(self,episode_list,author_list,podcast_object):
        episode = save_episode.delay(episode_list,author_list,podcast_object.id).get()
        return episode
