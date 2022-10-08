from atexit import register
from django import template
from users_data.models import WatchList
from youtube_app.models import Category, Keyword
register= template.Library()
@register.filter(name='VideoCategory')
def VideoCategory(string_value):
    all_keywords= Keyword.objects.all()
    # print('String#######', string_value)
    list=[]
    for keyword in all_keywords:
        # print('keyword#######', keyword.keyword)
        if keyword.keyword in string_value:
            # print('if temp', keyword.category.category)
            # print('if temp', keyword.category.category)
            return keyword.category.category
        elif keyword.keyword.upper() in string_value:
            return keyword.category.category
        elif keyword.keyword.lower() in string_value:
            return keyword.category.category
        else:
            # print('else')
            pass
            
            