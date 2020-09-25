import re
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import YoutubePlaylistItem, YoutubeVideos



def format_url(url, video=False, playlist=False):
    re_code = re.compile(r'https://www.youtube\.com/watch\?v=(?P<video_id>[\w\W\d]+)&list=(?P<pl_id>[\w\W]+)?(&index)')
    playlist_url = 'https://www.youtube.com/embed?listType=playlist&list='
    video_url = 'https://www.youtube.com/embed/'
    match = re.search(re_code, url)
    if match:
        if video:
            return video_url + match.group('video_id')
        elif playlist:
            return playlist_url + match.group('pl_id')


@receiver(pre_save, sender=YoutubePlaylistItem)
def playlist_url_func(sender, instance, **kwargs):
    instance.playlistUrl = format_url(instance.playlistUrl, playlist=True)
    
@receiver(pre_save, sender=YoutubeVideos)
def video_url_func(sender, instance, **kwargs):
    print(instance.videoUrl)
    print(format_url(instance.videoUrl, video=True))
    instance.videoUrl = format_url(instance.videoUrl, video=True)