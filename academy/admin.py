from django.contrib import admin
from embed_video.admin import AdminVideoMixin
from .models import (YoutubeVideos,
                     YoutubePlaylistItem,
                     YoutubePlaylist,
                     AcademyPrivateAnswer,
                     AcademyPrivateQuestion,
                     AcademyPublicAnswer,
                     AcademyPublicQuestion
                     )

# Register your models here.


class YoutubeAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass

admin.site.register(AcademyPrivateAnswer)
admin.site.register(AcademyPrivateQuestion)
admin.site.register(AcademyPublicAnswer)
admin.site.register(AcademyPublicQuestion)
admin.site.register(YoutubePlaylist)
admin.site.register(YoutubeVideos, YoutubeAdmin)
admin.site.register(YoutubePlaylistItem, YoutubeAdmin)
