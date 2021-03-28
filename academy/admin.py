from django.contrib import admin
from embed_video.admin import AdminVideoMixin
from django.template.loader import get_template
from django.utils.translation import gettext as _

from .models import (YoutubeVideos,
                     YoutubePlaylistItem,
                     YoutubePlaylist,
                     AcademyPrivateAnswer,
                     AcademyPrivateQuestion,
                     AcademyPublicAnswer,
                     AcademyPublicQuestion,
                     SupportSingle,
                     SupportCollection,
                     AcademyModel,
                     )


# Register your models here.


class SupportInline(admin.StackedInline):
    model = SupportSingle


@admin.register(SupportCollection)
class SupportAdmin(admin.ModelAdmin):
    inlines = [SupportInline]
    
    class Meta:
       model = SupportCollection
 
@admin.register(SupportSingle)
class SupportInline(admin.ModelAdmin):
    pass

class YoutubeAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass

admin.site.register(AcademyPrivateAnswer)
admin.site.register(AcademyPrivateQuestion)
admin.site.register(AcademyPublicAnswer)
admin.site.register(AcademyPublicQuestion)
admin.site.register(YoutubePlaylist)
admin.site.register(YoutubeVideos, YoutubeAdmin)
admin.site.register(YoutubePlaylistItem, YoutubeAdmin)
admin.site.register(AcademyModel)

