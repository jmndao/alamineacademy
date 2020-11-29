from django.contrib import admin
from embed_video.admin import AdminVideoMixin
from django.template.loader import get_template
from django.utils.translation import gettext as _

from .forms import SupportAdminForm
from .models import (YoutubeVideos,
                     YoutubePlaylistItem,
                     YoutubePlaylist,
                     AcademyPrivateAnswer,
                     AcademyPrivateQuestion,
                     AcademyPublicAnswer,
                     AcademyPublicQuestion,
                     SupportSingle,
                     SupportCollection,
                     AcademyModel
                     )

# Register your models here.


class SupportInline(admin.TabularInline):
    model = SupportCollection


@admin.register(SupportSingle)
class SupportAdmin(admin.ModelAdmin):
    form = SupportAdminForm
    inlines = [SupportInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.save_photos(form.instance)

class YoutubeAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass

admin.site.register(AcademyPrivateAnswer)
admin.site.register(AcademyPrivateQuestion)
admin.site.register(AcademyPublicAnswer)
admin.site.register(AcademyPublicQuestion)
admin.site.register(YoutubePlaylist)
admin.site.register(YoutubeVideos, YoutubeAdmin)
admin.site.register(YoutubePlaylistItem, YoutubeAdmin)
admin.site.register(SupportCollection)
admin.site.register(AcademyModel)
