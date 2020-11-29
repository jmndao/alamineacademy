from django.db import models
from django.utils import timezone
from embed_video.fields import EmbedVideoField

from PIL import Image


# Create your models here.


# def file_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/<file_type>/<filename>
#     return '{0}/{1}'.format(instance.file_type, filename)


class SupportSingle(models.Model):
    '''
        A model that hold file by one and link to the SupportsModel in
        order to create a hierarchical organization of multiple 
        supports in one directory

        -- title        : title of the course
        -- description  : description of the course
    '''

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    
    def __str__(self):
        return self.title

class SupportCollection(models.Model):

    support_single = models.ForeignKey(
        SupportSingle, on_delete=models.CASCADE, related_name="support"
    )
    supports_dir = models.FileField(upload_to='supports/', null=True)

    def __str__(self):
        return self.support_single.title


class AcademyModel(models.Model):

    '''
        AcademyModel is the representative of differents feed 
        in AlAmineAcademy website that is designed to provide
        courses in islamic domains such as Seerah, Tawhid, etc 
        (see models.TextChoices)

            -- category     : Category of course to provide
            -- title        : title of the course
            -- description  : description of the course
            -- created_date : the date it is added in the site
    '''

    CATEGORY_TYPE = [
        ('SEERAH', 'Seerah'),
        ('TAWHID', 'Tawhid'),
        ('HADITHS', 'Hadiths'),
        ('KHUTBA', 'Khutba'),
        ('FIQH', 'Fiqh'),
        ('TAFSIR', 'Tafsir'),
        ('BAYANE', 'Bayane')
    ]

    title = models.CharField(max_length=250)
    description = models.TextField(default=None)
    price = models.DecimalField(max_digits=10, decimal_places=6)
    category = models.CharField(max_length=10, choices=CATEGORY_TYPE)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True)
    videos_dirs = models.FileField(
        upload_to='videos/', null=True, verbose_name="Videos")
    supports_dirs = models.ForeignKey(
        SupportCollection, default=None, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    def save(self):
        super().save()
        
        img = Image.open(self.thumbnail.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.thumbnail.path)

class AcademyPublicQuestion(models.Model):
    '''
        AcademyPublicQA is a model that describe a Public 
        platform for Question and Answer.
        An anonymous user will ask a question that anyone 
        will be able to see in the site and the answer if 
        answered (by the admin)

        -- question_text    : the question
        -- date_posted      : the date the question was asked
    '''

    username  = models.CharField(max_length=50)
    questionText = models.TextField()
    datePosted = models.DateTimeField(auto_now_add=True)


class AcademyPublicAnswer(models.Model):
    '''
        AcademyPublicQA is a model that describe a Public 
        platform for Question and Answer.
        An anonymous user will ask a question that anyone 
        will be able to see in the site and the answer if 
        answered (by the admin)

        -- question     : foreign_key that link the answer to the question
        -- answer       : the answer (by the admin)
        -- answer_date  : the date the question is answered

    '''

    question = models.ForeignKey(
        AcademyPublicQuestion, on_delete=models.CASCADE)
    answer = models.TextField()
    answerDate = models.DateTimeField(auto_now_add=True)


class AcademyPrivateQuestion(models.Model):

    '''
        AcademyPrivateQA is a model that describe a Private 
        platform for Question and Answer.
        An anonymous user will ask a question that a dedicated 
        answer will be sent to his email box (by the admin)

        -- question_text   : the question
        -- email           : the address email
        -- sexe            : the sexe (male or female) 

    '''

    SEXES = (
        ('F', 'Female'),
        ('M', 'Male'),
        ('N', 'Neutral')
    )

    question_text = models.TextField()
    email = models.EmailField()
    sexe = models.CharField(max_length=2, choices=SEXES)


class AcademyPrivateAnswer(models.Model):
    '''
        AcademyPrivateQA is a model that describe a Private 
        platform for Question and Answer.
        An anonymous user will ask a question that a dedicated 
        answer will be sent to his email box (by the admin)

        -- question    : the question that was asked by a Private guest
        -- answer      : answer to the question
        -- answer_date : the date the question was answered

    '''

    question = models.ForeignKey(
        AcademyPrivateQuestion, on_delete=models.CASCADE)
    answer = models.TextField()
    answerDate = models.DateTimeField(auto_now_add=True)


class YoutubePlaylist(models.Model):
    '''
        A model that record playlists

        -- title        : title of the playlist
    '''

    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class YoutubePlaylistItem(models.Model):
    '''
        A model that keep track of videos' playlist then 
        indicates in which category (see below list) the 
        playlist belongs to.

        -- title        : title of the playlist
        -- category     : category to which belongs the playlist

    '''
    CATEGORY_TYPE = [
        ('SEERAH', 'Seerah'),
        ('TAWHID', 'Tawhid'),
        ('HADITHS', 'Hadiths'),
        ('KHUTBA', 'Khutba'),
        ('FIQH', 'Fiqh'),
        ('TAFSIR', 'Tafsir'),
        ('BAYANE', 'Bayane')
    ]

    category = models.CharField(max_length=10, choices=CATEGORY_TYPE)
    playlist = models.ForeignKey(YoutubePlaylist, on_delete=models.CASCADE)
    playlistUrl = EmbedVideoField(default=None, blank=True)


class YoutubeVideos(models.Model):

    '''
        A model that held record of youtube videos on the
        website via the django-embed-video framework. 
        We'll be able to embed youtube video in the website
        easily with track of their playlist too. 

        -- title        : title of the video
        -- description  : description of the video
        -- videos       : videos' urls
        -- playlist     : each video belongs to a playlist
                          (YoutubePlaylist_class)
    '''

    title = models.CharField(max_length=100)
    description = models.TextField()
    videoUrl = EmbedVideoField()
    playlist = models.ForeignKey(YoutubePlaylist, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
