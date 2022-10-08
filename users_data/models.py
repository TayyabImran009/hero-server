import imp
from django.db import models
from django.contrib.auth.models import User
from youtube_app.models import*

# Create your models here.

class FollowedAthletes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followed_athlete = models.ForeignKey(AthleteProfile, on_delete=models.CASCADE)
    class Meta:
        verbose_name = ("Followed Athlete")
        verbose_name_plural = ("Followed Athletes")
    def __str__(self) :
        return str(self.user.username)


class FollowedCommunity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followed_community = models.ForeignKey(CommunityProfile, on_delete=models.CASCADE)
    class Meta:
        verbose_name = ("Followed Community")
        verbose_name_plural = ("Followed Community")
    def __str__(self) :
        return str(self.user.username)


class FollowPersonality(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    keyword= models.ForeignKey(Keyword, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.keyword.keyword)
    def __str__(self):
        return "{0}".format(self.keyword.keyword)


class WatchList(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    video_title= models.CharField(max_length=300)
    video_description= models.CharField(max_length= 1000)
    video_id= models.CharField(max_length= 20)
    channel_title= models.CharField(max_length=100)
    upload_date=models.CharField(max_length=100)
    channel_profile_pic= models.CharField(max_length=100)
    video_thumbnail_pic= models.CharField(max_length=100)
