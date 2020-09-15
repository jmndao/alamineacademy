from django.db import models
from django.utils import timezone
from embed_video.fields import EmbedVideoField

# Create your models here.


def file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<file_type>/<filename>
    return '{0}/{1}'.format(instance.file_type, filename)


class AcademyModel(models.Model):

    '''
        AcademyModel is the representative of differents feed 
        in AlAmineAcademy website that is designed to provide
        courses in islamic domains such as Seerah, Tawhid, etc 
        (see models.TextChoices)

            -- category     : Category of course to provide
            -- title        : title of the course
            -- description  : description of the course
            -- file_type    : type of the file (audio or video)
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

    category = models.CharField(blank=True, choices=CATEGORY_TYPE, max_length=10)
    title = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField()
    file_type_choices = models.TextChoices('audio', 'video')
    file_type = models.CharField(blank=True, choices=file_type_choices.choices, max_length=10)
    upload = models.FileField(upload_to=file_directory_path)
    created_date = models.DateTimeField(default=timezone.now)


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

    question_text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

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

    question = models.ForeignKey(AcademyPublicQuestion, on_delete=models.CASCADE)
    answer = models.TextField()
    answer_date = models.DateTimeField(auto_now_add=True)
    


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
        ('M', 'Male')
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

    question = models.ForeignKey(AcademyPrivateQuestion, on_delete=models.CASCADE)
    answer = models.TextField()
    answer_date = models.DateTimeField(auto_now_add=True)

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
        A model that keep track of videos' playlist. 
        
        -- title        : title of the playlist
        
    '''
    
    playlist_title = models.ForeignKey(YoutubePlaylist, on_delete=models.CASCADE)
    playlist_url = EmbedVideoField()
    

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
    video_url = EmbedVideoField()
    playlist = models.ForeignKey(YoutubePlaylist, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title