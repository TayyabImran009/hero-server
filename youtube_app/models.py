from ast import keyword
from email.policy import default
from pyexpat import model
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField





# TODO: Must Read!!!!!!!!!!!!
# TODO: If you add another model class then must add this model in settings.py/ADMIN_REORDER to view it in Django Admin section either create a new Group or add in existing one.


class Category(models.Model):
    category= models.CharField(max_length=40)
    order_of_display=models.IntegerField(default=0)
    is_random = models.BooleanField(default=False)
    class Meta:
        verbose_name = ("Lane")
        verbose_name_plural = ("Lanes")
    def __str__(self):
        return u'{0}'.format(self.category)

        
class Keyword(models.Model):
    category= models.ForeignKey(Category, on_delete=models.CASCADE)
    keyword= models.CharField(max_length=50, null= True, blank=True)
    channel_id= models.CharField(max_length=100, default= '', null= True, blank= True)
    image = models.ImageField(verbose_name='Image',null=True, blank=True, upload_to="upload_images/")
    data=JSONField(null= True, blank=True)
    most_recent= models.BooleanField(default=True)
    disable = models.BooleanField(default=False)
    def __str__(self):
        return u'{0}'.format("K-W ="+str(self.keyword)+" C-ID ="+str(self.channel_id))

class AllData(models.Model):
    data= JSONField(null=True, blank=True)


# Random categories
# class RandomCategory(models.Model):
    # category_name= models.CharField(max_length=40)
    # order_of_display=models.IntegerField(default=0)
    # def __str__(self):
    #     return u'{0}'.format(self.category_name)

# Add Random Video in Database to show on your page
class RandomVideo(models.Model):
    category= models.ForeignKey(Category,on_delete=models.CASCADE, blank=True, null=True)
    # category= models.ForeignKey(RandomCategory,on_delete=models.CASCADE, blank=True, null=True)
    video_title= models.CharField(max_length=300)
    video_description= models.CharField(max_length= 600)
    video_id= models.CharField(max_length= 20)
    channel_title= models.CharField(verbose_name="Channel Title (Optional) ",max_length=100, null=True, blank=True)
    upload_date=models.CharField( verbose_name="Uploaded Date (Optional) ",max_length=100, null=True, blank=True)
    channel_id= models.CharField(verbose_name="Channel ID (Optional) ",max_length=100, null=True, blank=True)
    video_thumbnail_pic_url= models.URLField(max_length=200, default='', null=True, blank=True)
    video_thumbnail_pic_local = models.ImageField(verbose_name='Thumbnail Image',null=True, blank=True, upload_to="upload_images/")
    
    class Meta:
        verbose_name = ("Managed Video")
        verbose_name_plural = ("Managed Videos")    

class HeroSection(models.Model):
    video_title= models.CharField(max_length=300 , default='')
    video_description= models.CharField(max_length= 600, default='')
    video_id= models.CharField(max_length= 20, default='')
    channel_title= models.CharField(max_length=100, default='')
    upload_date=models.CharField(max_length=100, default='')
    channel_id= models.CharField(max_length=100, default='')
    background_image_url= models.URLField(max_length=200 , default='')
    class Meta:
        verbose_name = ("Hero Corousel")
        verbose_name_plural = ("Hero Corousels") 
    

  
# Athletes Profile
# 1- Athletes profile categories
class AthleteProfileCategory(models.Model):
    id= models.BigIntegerField(primary_key=True)
    category_name = models.CharField(max_length=300, default='')
    def __str__(self) :
        return str(self.category_name)
    class Meta:
        verbose_name = ("Athlete Profile Categories")
        verbose_name_plural = (" Athlete Profile Categories")

class AthleteProfile(models.Model):
    name = models.CharField(max_length=1000, blank=True)
    profile_category= models.ForeignKey(AthleteProfileCategory, on_delete=models.CASCADE, blank=True, null=True)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    avatar_image = models.ImageField(verbose_name='Avatar', upload_to="upload_images/", default="upload_images/default.png")
    banner_image = models.ImageField(verbose_name='Banner Image',null=True, blank=True, upload_to="upload_images/")
    age = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    experience = models.CharField(max_length=400, null=True, blank=True)
    bio = models.CharField(max_length=500)
    class Meta:
        verbose_name = ("Athlete Profiles")
        verbose_name_plural = ("Athlete Profiles")


    def __str__(self) :
        if self.keyword.keyword:
            return str(self.keyword.keyword)
        else:
            return str(self.keyword.channel_id)


# Community Profile
# 1- Community profile categories
class CommunityProfileCategory(models.Model):
    id= models.BigIntegerField(primary_key=True)
    category_name = models.CharField(max_length=300, default='')
    def __str__(self) :
        return str(self.category_name)
    class Meta:
        verbose_name = ("community Profile Categories")
        verbose_name_plural = ("community Profile Categories")

class CommunityProfile(models.Model):
    name = models.CharField(max_length=1000, blank=True)
    profile_category= models.ForeignKey(CommunityProfileCategory, on_delete=models.CASCADE, blank=True, null=True)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    avatar_image = models.ImageField(verbose_name='Avatar',null=True, blank=True, upload_to="upload_images/")
    banner_image = models.ImageField(verbose_name='Banner Image', upload_to="upload_images/", default="upload_images/default.png")
    age = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    experience = models.CharField(max_length=400, null=True, blank=True)
    bio = models.CharField(max_length=500)
    class Meta:
        verbose_name = ("Community Profiles")
        verbose_name_plural = ("Community Profiles")


    def __str__(self) :
        if self.keyword.keyword:
            return str(self.keyword.keyword)
        else:
            return str(self.keyword.channel_id)

        

class BlackListVideos(models.Model):
    video_id = models.CharField(max_length=400,null=True, blank=True)
    channel_id = models.CharField(max_length=400,null=True, blank=True)

    def __str__(self) :
        return str("VideoID="+str(self.video_id)+"ChannelID="+str(self.channel_id))




