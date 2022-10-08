from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from django.contrib import admin

from youtube_app.models import *

# Register your models here.


# *************************************************************************** Random Video


class RandomVideoResource(resources.ModelResource):

    class Meta:
        model = RandomVideo
    

class RandomVideoAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('id','category', 'video_title', 'video_description', 'video_id', 'channel_title', 'upload_date', 'channel_id', 'video_thumbnail_pic_url', 'video_thumbnail_pic_local')

    resource_class = RandomVideoResource


    # ******************** For filtering categories which have is_random field True
    def get_form(self, request, obj=None, **kwargs):
        form = super(RandomVideoAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['category'].queryset = Category.objects.filter(is_random = 'True')
        return form


admin.site.register(RandomVideo, RandomVideoAdmin)


# *************************************************************************** Keywords


# ************* Filter to make most_recent = False for all quersets 
# @admin.action(description='Remove videos from most recent')
# def remove_recent(modeladmin, request, queryset):
#     queryset.update(most_recent='False')
#
class KeywordResource(resources.ModelResource):
    class Meta:
        # for Showing foreign key data in foreign key field
        model = Keyword
        # import_id_fields = ('category',)
        # subject = fields.Field(
        #     column_name='category',
        #     attribute='category',
        #     widget=ForeignKeyWidget(Category, 'category'))
            
class KeywordAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('id','category', 'keyword', 'channel_id','image', 'most_recent')
    # ************** Filter Data according to different categories and most recent. Just add the field name to filter by the field 
    # list_filter = ('most_recent','category')
    # actions = [remove_recent]

    resource_class = KeywordResource

    # # ******************** For filtering categories which have is_random field True
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(KeywordAdmin, self).get_form(request, obj, **kwargs)
    #     form.base_fields['category'].queryset = Category.objects.filter(is_random = 'False')
    #     return form

admin.site.register(Keyword, KeywordAdmin)

# *************************************************************************** Hero Selection

class HeroSectionResource(resources.ModelResource):

    class Meta:
        model = HeroSection

class HeroAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('id','video_title', 'video_description', 'video_id','channel_title', 'upload_date', 'channel_id', 'background_image_url')

    resource_class = HeroSectionResource

    def has_add_permission(self, request):
        base_add_permission = super(HeroAdmin, self).has_add_permission(request)
        if base_add_permission:
            # if there's already an entry, do not allow adding
            count = HeroSection.objects.all().count()
            if count == 0:
                return True
        return False

admin.site.register(HeroSection, HeroAdmin)

# *************************************************************************** Hero Category

class CategoryResource(resources.ModelResource):

    class Meta:
        model = Category


class CategoryAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('id', 'category', 'order_of_display', 'is_random')
    verbose_name = ("Lanes")
    resource_class = CategoryResource
    
        


admin.site.register(Category,CategoryAdmin)
# *******************************************************************************************************************************************


admin.site.register(AllData)

# admin.site.register(RandomCategory, RandomCategoryAdmin)

# **************************************************************************Athlete Profile
class AthleteProfileAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('keyword','avatar_image','banner_image','age','country','experience','bio')
    def get_form(self, request, obj=None, **kwargs):
        form = super(AthleteProfileAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['keyword'].queryset = Keyword.objects.filter(disable = 'False')
        return form

admin.site.register(AthleteProfile,AthleteProfileAdmin)

admin.site.register(AthleteProfileCategory)



# ***************************************************************************Community Profile

class CommunityProfileAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('keyword','avatar_image','banner_image','age','country','experience','bio')
    def get_form(self, request, obj=None, **kwargs):
        # request = kwargs['request']
        form1 = super(CommunityProfileAdmin, self).get_form(request, obj, **kwargs)
        form1.base_fields['keyword'].queryset = Keyword.objects.filter(disable = 'False')
        return form1
admin.site.register(CommunityProfile,CommunityProfileAdmin)

admin.site.register(CommunityProfileCategory)


admin.site.register(BlackListVideos)