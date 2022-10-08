from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *
# Register your models here.


# *************************************************************************** Watch List

class WatchListResource(resources.ModelResource):

    class Meta:
        model = WatchList

class WatchListAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('id','user','video_title','video_description','video_id','channel_title','upload_date','channel_profile_pic','video_thumbnail_pic')
    resource_class = WatchListResource

admin.site.register(WatchList, WatchListAdmin)


class FollowedAthletesAdmin(admin.ModelAdmin):
    list_display = ('user','followed_athlete')

admin.site.register(FollowedAthletes,FollowedAthletesAdmin)

admin.site.register(FollowPersonality)

class FollowedCommunityAdmin(admin.ModelAdmin):
    list_display = ('user','followed_community')

admin.site.register(FollowedCommunity,FollowedCommunityAdmin)