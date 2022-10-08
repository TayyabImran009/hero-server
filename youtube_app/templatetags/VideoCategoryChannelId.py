from atexit import register
from django import template
from users_data.models import WatchList
from youtube_app.models import Category, Keyword
register= template.Library()
@register.filter(name='VideoCategoryChannelId')
def VideoCategoryChannelId(string_value):
    all_keywords= Keyword.objects.all()
    
    list=[]
    for keyword in all_keywords:
        # print('Channel filter#######', keyword.keyword)
        if keyword.channel_id == string_value:
            # print('String####### channel', string_value, keyword.channel_id)
            # print('if temp video channel', keyword.category.category)
            return keyword.category.category
        
        else:
            # print('else')
            pass
            
            