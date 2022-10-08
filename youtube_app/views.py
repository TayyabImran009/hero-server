from multiprocessing import context
from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render,redirect

from .models import *
from users_data.models import*
from googleapiclient.discovery import build
from django.contrib.auth.models import User
import datetime
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.core.paginator import Paginator
import random
from django.contrib.auth.decorators import login_required


# Youtube API Key
api_key= 'AIzaSyAzaAIFiU2QKcD4sqC47j-I9-0fAk3awHw'
api_key_2='AIzaSyAo9njxj8OJpWshmpCyamYf9GJXN-kIi64'
api_key_3='AIzaSyBztkmRfxkYWS9QCtS9XD8r6clecRBVK2s'
api_key_4='AIzaSyA4Mt5QJqtcTJ77BHIeFAj12M6s5mSUiFQ'
api_key_5='AIzaSyA6aQiZykCZBYzGheYaKYdJYPKUsAQrrCs'
api_key_6= 'AIzaSyAczxkO9D2vorvtomWQwtGLEnQ2FjmRdjk'

youtube = build('youtube', 'v3', developerKey=api_key_2)
# Create your views here.
def register(request):
    if request.method== 'POST':
        fullname= request.POST.get('name')
        username= request.POST.get('username')
        email= request.POST.get('email')
        password= request.POST.get('password')
        if User.objects.filter(username=username):
            return redirect('/register')
        user_obj= User(username=username, email=email, first_name= fullname) 
        user_obj.set_password(password)
        user_obj.save()
        user = authenticate(username=username, password=password)
        login(request, user)
        
        return redirect('/home')
    return render(request, 'users/register.html')
def loginUser(request):
        if request.user.is_authenticated:
            return redirect('/home')
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            try:
                user = User.objects.get(username=username)
            except:
                 return redirect('/')
            if user:

                username = user.username
                user = authenticate(request, username=username, password=password) # check password

            if user is not None:
                login(request, user)
                return redirect('/home')	
            
        return render(request,'users/login.html',)

def logoutUser(request):
        print('1212122')
        logout(request)
        return redirect('/')


def home(request):
    context={}
    try:
        data_list=[]
        paginator_list=[]
        paginator_list_2=[]
        # all_data_obj=AllData.objects.get(id=1)
        categories= Category.objects.all().order_by('order_of_display')
        index=0
        for category in categories:
            print("category*********************************************************",category)
            if not category.is_random:
                print("category*********************************************************",category)
                try:
                    first_data_list=[]
                    unfollow_keyword_data_list=[]
                    follow_keyword_data_list = []
                    follower_keyword_list=[]
                    followed_obj= FollowPersonality.objects.filter(user=request.user,keyword__category__category=category)
                    print('followed_obj', followed_obj)
                    if followed_obj.exists():
                        for follower in followed_obj:
                            first_data_list += follower.keyword.data
                            follower_keyword_list.append(follower.keyword.keyword)
                        follower_keyword_list = sorted(follower_keyword_list, key=lambda x: (x['snippet']['publishedAt']), reverse=True)
                    keyword_obj= Keyword.objects.filter(category__category=category).exclude(keyword__in=follower_keyword_list)
                    for key in keyword_obj:
                        print('Keyword', key.keyword)
                        unfollow_keyword_data_list += key.data 
                        random.shuffle(unfollow_keyword_data_list)
                    unfollow_keyword_data_list = sorted(unfollow_keyword_data_list, key=lambda x: (x['snippet']['publishedAt']), reverse=True)
                    first_data_list = first_data_list+ unfollow_keyword_data_list
                    paginator = Paginator(first_data_list, 1)
                    page = request.GET.get('page', 1)
                    keywords = paginator.get_page(page)
                    
                    for key_d in keywords:
                        print('Data', key_d)
                    paginator_list+=keywords
                    
                    obj_1=keyword_obj[0]
                    # obj_2=keyword_obj[1]
                    # print('keyword obj',obj_2)
                
                    data_list= data_list+obj_1.data
                    # data_list= data_list+obj_2.data
                    
                    index+=1
                except Exception as e:
                    print(e)
                    pass
        # print('Paginator', paginator_list)
        # all_data_obj=Keyword.objects.get(id=1)
        # data_list=data_list+all_data_obj.data
        # data_list= data_list+video_items
        # print(video_items)
        # ********************** All recent videos
        most_recent_data_list=[]
        most_recent_keywords_obj= Keyword.objects.filter(most_recent=True).order_by('-id')
        for most_recent in most_recent_keywords_obj:
            try:
                if not most_recent.disable:
                    most_recent_data_list = most_recent_data_list + most_recent.data
            except:
                pass
        most_recent_sorted_by_date =sorted(most_recent_data_list, key=lambda x: (x['snippet']['publishedAt']), reverse=True)
        paginator_recent = Paginator(most_recent_sorted_by_date,20)
        page_recent = request.GET.get('page', 1)
        most_recent_keywords = paginator_recent.get_page(page_recent)
        
        # *********************** Saved videos list
    
        watchlist_videos= WatchList.objects.filter(user=request.user)
        videos_id_list=[]
        
        # ********************* Watch list videos
        for video in watchlist_videos:
            videos_id_list.append(video.video_id)
            

        
        # ********************* Random Video
        random_videos = RandomVideo.objects.all()
        if not random_videos.exists():
            print('**************No random video')
            random_videos = ""
        # ********************** Hero section background
        hero_section = HeroSection.objects.all().first()   
        # print(video_response)

        # ********************** Followed athletes data
        followed_athletes_data_list = []
        followed_athletes_obj = FollowedAthletes.objects.filter(user=request.user).order_by('id')
        print('followed atletes**************', followed_athletes_obj )
        for followed_athlete in followed_athletes_obj:
            if followed_athlete.followed_athlete.keyword.data:
                followed_athletes_data_list += followed_athlete.followed_athlete.keyword.data

        followed_athletes_data_list = sorted(followed_athletes_data_list, key=lambda x: x['snippet']['publishedAt'])

        
        # ********************** Followed Community data
        followed_community_data_list = []
        followed_community_obj = FollowedCommunity.objects.filter(user=request.user).order_by('id')
        print('followed atletes**************', followed_community_obj )
        for followed_community in followed_community_obj:
            if followed_community.followed_community.keyword.data:
                followed_community_data_list += followed_community.followed_community.keyword.data

        followed_community_data_list = sorted(followed_community_data_list, key=lambda x: x['snippet']['publishedAt'])

        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

        context= {
            'data': paginator_list,
            'watchlist_videos': videos_id_list,
            'categories':categories, 
            'keywords_page_info':keywords, 
            'most_recent': most_recent_keywords, 
            'all_random_videos':random_videos, 
            'hero_section':hero_section,
            'followed_athletes':followed_athletes_data_list,
            'watchlist_videos_data': watchlist_videos,
            'followed_community':followed_community_data_list
            }
    except:
        pass
    return render(request, 'youtube/home.html', context)

def dummy_home_2(request):
    data_list=[]
    paginator_list=[]
    paginator_list_2=[]
    # all_data_obj=AllData.objects.get(id=1)
    categories= Category.objects.all()
    index=0
    for category in categories:
        try:
            first_data_list=[]
            follower_keyword_list=[]
            followed_obj= FollowPersonality.objects.filter(keyword__category__catgeory=category)
            if followed_obj.exists():
                for follower in followed_obj:
                    first_data_list += follower.keyword.data
                    follower_keyword_list.append(follower.keyword.keyword)

            keyword_obj= Keyword.objects.filter(category__category=category).exclude(keyword__in=follower_keyword_list)
            
            paginator = Paginator(keyword_obj, 2)
            page = request.GET.get('page', 1)
            keywords = paginator.get_page(page)
            for key in keywords:
                paginator_list = paginator_list+ key.data
            obj_1=keyword_obj[0]
            # obj_2=keyword_obj[1]
            # print('keyword obj',obj_2)
        
            data_list= data_list+obj_1.data
            # data_list= data_list+obj_2.data
            
            index+=1
        except:
            pass
    print('Paginator', paginator_list)
    # all_data_obj=Keyword.objects.get(id=1)
    # data_list=data_list+all_data_obj.data
    # data_list= data_list+video_items
    # print(video_items)
    
    watchlist_videos= WatchList.objects.filter(user=request.user)
    videos_id_list=[]
    for video in watchlist_videos:
        videos_id_list.append(video.video_id)

    
    # print(video_response)
    context= {'data': paginator_list, 'watchlist_videos': videos_id_list, 'categories':categories, 'keywords_page_info':keywords}
    return render(request, 'youtube/home.html', context)

# AJAX Call to get data of remaining Objects
@csrf_exempt
def home_data_ajax(request):
    try:
            videos_id_list_watchlist=[]
            watchlist_videos= WatchList.objects.filter(user=request.user)
            
            for video in watchlist_videos:
                videos_id_list_watchlist.append(video.video_id)
    except Exception as e:
            print(e)
            pass
    try:
        if request.method == "POST":
            print('post req')
            page_number= request.POST.get('page_number') 
            next_page= int(page_number)+1
            category_name= request.POST.get('category_name') 
            print('page_number',page_number)
            print('next_page',next_page)
            print('category_name',category_name)
            first_data_list=[]
            follower_keyword_list=[]
            unfollow_keyword_data_list = []
            followed_obj= FollowPersonality.objects.filter(user=request.user,keyword__category__category=category_name)
            if followed_obj.exists():
                for follower in followed_obj:
                    if not follower.keyword.disable:
                        first_data_list += follower.keyword.data
                        follower_keyword_list.append(follower.keyword.keyword)
            first_data_list = sorted(first_data_list, key=lambda x: (x['snippet']['publishedAt']), reverse=True)
            
            keyword_obj= Keyword.objects.filter(category__category=category_name).exclude(keyword__in=follower_keyword_list)
            for key in keyword_obj:
                print(key.data)
                try:
                    if not key.disable:
                        unfollow_keyword_data_list += key.data 
                except:
                    pass
                random.shuffle(unfollow_keyword_data_list)
            unfollow_keyword_data_list = sorted(unfollow_keyword_data_list, key=lambda x: (x['snippet']['publishedAt']), reverse=True)
            first_data_list = first_data_list+ unfollow_keyword_data_list
            paginator = Paginator(first_data_list, 20)
            page = request.GET.get('page', next_page)
            keywords = paginator.get_page(page)
            paginator_list=[]
            paginator_list+=keywords
            return JsonResponse({'data': paginator_list, 'page_number': next_page,'videos_id_list':videos_id_list_watchlist})
    except:
        pass
# AJAX Call to get data of remaining recent Objects
@csrf_exempt
def home_data_recent_ajax(request):
    try:
            videos_id_list_watchlist=[]
            watchlist_videos= WatchList.objects.filter(user=request.user)
            
            for video in watchlist_videos:
                videos_id_list_watchlist.append(video.video_id)
    except Exception as e:
            print(e)
            pass
    try:
        if request.method == "POST":
            print('post req')
            page_number= request.POST.get('page_number') 
            next_page= int(page_number)+1
            category_name= request.POST.get('category_name') 
            print('page_number',page_number)
            print('next_page',next_page)
            print('category_name',category_name)
            # ***************************************** Most recent method
            most_recent_data_list=[]
            most_recent_keywords_obj= Keyword.objects.filter(most_recent=True).order_by('-id')
            for most_recent in most_recent_keywords_obj:
                try:
                    if not most_recent.disable:
                        most_recent_data_list = most_recent_data_list + most_recent.data
                except:
                    pass
            most_recent_sorted_by_date =sorted(most_recent_data_list, key=lambda x: (x['snippet']['publishedAt']), reverse=True)
            paginator_recent = Paginator(most_recent_sorted_by_date,20)
            page_recent = request.GET.get('page', next_page)
            most_recent_keywords = paginator_recent.get_page(page_recent)
            print(most_recent_sorted_by_date)
            # ************************************************ End
            first_data_list=[]
            keyword_obj= Keyword.objects.filter(most_recent=True)
            # for key in keyword_obj:
            #     first_data_list = first_data_list+ key.data
            paginator = Paginator(keyword_obj, 2)
            page = request.GET.get('page', next_page)
            keywords = paginator.get_page(page)
            for key in keywords:
                first_data_list = first_data_list+ key.data
            paginator_list=[]
            paginator_list+=most_recent_keywords
            return JsonResponse({'data': paginator_list, 'page_number': next_page,'videos_id_list':videos_id_list_watchlist})
    except:
        pass
# Add data in home page on load AJAX
@csrf_exempt
def add_data_home_onload(request):
    try:
            videos_id_list_watchlist=[]
            watchlist_videos= WatchList.objects.filter(user=request.user)
            
            for video in watchlist_videos:
                videos_id_list_watchlist.append(video.video_id)
    except Exception as e:
            print(e)
            pass
    try:
        if request.method == 'POST':
            filter_category= request.POST.get('filter_category')
            filter= request.POST.get('filter')
            filter_type=type_of_filter(filter)
            # print('category', filter_category)
            # print('filter',filter)
            # print('type_of_filter(filter)', type_of_filter(filter))
            unfollow_keyword_data_list = []
            first_data_list=[]
            follower_keyword_list=[]
            followed_obj= FollowPersonality.objects.filter(user=request.user,keyword__category__category=filter_category)
            if followed_obj.exists():
                for follower in followed_obj:
                    try:
                        if not follower.keyword.disable:
                            first_data_list += follower.keyword.data
                    except:
                        pass
                    follower_keyword_list.append(follower.keyword.keyword)
            first_data_list = sorted(first_data_list, key=lambda x: (x['snippet']['publishedAt']), reverse=True)
                
            keyword_obj= Keyword.objects.filter(category__category=filter_category).exclude(keyword__in=follower_keyword_list)
            paginator_list=[]
            # print('Keyword object', keyword_obj)
            for key in keyword_obj:
                # print(key.data)
                try:
                    if not key.disable:
                        unfollow_keyword_data_list += key.data 
                except:
                    pass
                random.shuffle(unfollow_keyword_data_list)
            unfollow_keyword_data_list = sorted(unfollow_keyword_data_list, key=lambda x: (x['snippet']['publishedAt']), reverse=True)
            first_data_list = first_data_list+ unfollow_keyword_data_list
            sorted_list = first_data_list
            paginator = Paginator(first_data_list, 20)
            page = request.GET.get('page', 1)
            keywords = paginator.get_page(page)
            
            # for key_d in keywords:
            #     print('Data', key_d)
            paginator_list+=keywords
            # print(sorted_list)
        return JsonResponse({'data': paginator_list, 'videos_id_list':videos_id_list_watchlist})
    except:
        pass

def home_data_ajax_dummy(request):
    try:
            videos_id_list_watchlist=[]
            watchlist_videos= WatchList.objects.filter(user=request.user)
            
            for video in watchlist_videos:
                videos_id_list_watchlist.append(video.video_id)
    except Exception as e:
            print(e)
            pass
    if request.method == "POST":
        print('post req')
        page_number= request.POST.get('page_number') 
        next_page= int(page_number)+1
        category_name= request.POST.get('category_name') 
        print('page_number',page_number)
        print('next_page',next_page)
        print('category_name',category_name)
        keyword_obj= Keyword.objects.filter(category__category=category_name )
        
        paginator = Paginator(keyword_obj, 2)
        page = request.GET.get('page', next_page)
        keywords = paginator.get_page(page)
        paginator_list=[]
        for key in keywords:
            paginator_list = paginator_list+ key.data
        return JsonResponse({'data': paginator_list, 'page_number': next_page,'videos_id_list':videos_id_list_watchlist})

def dummy_home(request):
    # api_key = '#YOURAPIKEY'

   

    # request1 = youtube.channels().list(
    #         part='contentDetails',
    #         forUsername='schafer5'
    #     )
    # request_channel_snippet = youtube.channels().list(
    #         part='snippet',
    #         forUsername='schafer5' 
    #     )

    # response = request1.execute()
    # response_channel_snippet=request_channel_snippet.execute()
    # # print('response****************',response)
    # items=response['items']
    # snippet_items= response_channel_snippet['items']
    # snippet_item= snippet_items[0]
    # profile_picture= snippet_item['snippet']['thumbnails']['default']['url']

    # item=items[0]
    # content= item['contentDetails']
    # playlist= content['relatedPlaylists']
    # uploads=playlist['uploads']
    # print(response)
    # print(uploads)
    # all_keywords= Keyword.objects.all()
    keyword_var=''
    data_list= []   
    all_keywords_updated= Keyword.objects.all() 
    for keyword in all_keywords_updated:
        data_list=data_list+keyword.data
        # data_list= data_list+video_items
    # print(video_items)
    
    watchlist_videos= WatchList.objects.filter(user=request.user)
    videos_id_list=[]
    for video in watchlist_videos:
        videos_id_list.append(video.video_id)

    categories= Category.objects.all
    # print(video_response)
    context= {'data': data_list, 'watchlist_videos': videos_id_list, 'categories':categories}
    return render(request, 'youtube/home.html', context)

def video_view(request):
    
  
    if request.method == 'POST':
        video_description= request.POST.get('video_description')
        video_title= request.POST.get('video_title')
        video_id= request.POST.get('video_id')
        channel_title= request.POST.get('channel_title')
        # channel_profile= request.POST.get('channel_id')
        # print('video_id', video_id)
        # ************************** Getting video statistics
        
        request_video_statistics = youtube.videos().list(
                        part="statistics,snippet",
                        id=video_id,
                        maxResults=1
                        )
        response_video_statistics = request_video_statistics.execute()
        video_statistic_items= response_video_statistics['items']
        channel_profile = video_statistic_items[0]['snippet']['channelId']
        # *************************** To get the channel profile pic
        request_channel_snippet = youtube.channels().list(
            part='snippet',
            id=channel_profile 
        )
        response_channel_snippet=request_channel_snippet.execute()
        snippet_items= response_channel_snippet['items']
        snippet_item= snippet_items[0]
        profile_picture= snippet_item['snippet']['thumbnails']['default']['url']
        # End profile picture
        
        
        # *********************** Getting video data 
        video_date = video_statistic_items[0]['snippet']['publishedAt']
        # video_date= request.POST.get('video_date')
        d1 = datetime.datetime.strptime(video_date,"%Y-%m-%dT%H:%M:%SZ")

        
        # ***************** Getting related videos *********************
        video_request = youtube.search().list(
        part='snippet',
        type='video',
        channelId= channel_profile,
        maxResults= 50
        ) 
        video_reponse= video_request.execute()
        related_videos =  video_reponse['items']

        # ***************** List of videos in watchlist *************
        watchlist_videos= WatchList.objects.filter(user=request.user)
        videos_id_list=[]
        for video in watchlist_videos:
            videos_id_list.append(video.video_id)

        print('video_statistic_items****', video_statistic_items[0]['snippet']['description'])
        new_format = "%Y-%m-%d"
        upload_date=(d1.strftime(new_format))
    context = {
        'video_description': video_description,
        'video_title': video_title, 
        'video_id': video_id, 
        'channel_title': channel_title, 
        'channel_profile': profile_picture, 
        'upload_date': d1, 
        'video_statistics': video_statistic_items,
        'related_videos': related_videos,
        'watchlist_videos': videos_id_list
        }
    return render(request, 'youtube/video_player.html', context)

@csrf_exempt
def add_to_watchlist(request):
    if request.method == 'POST':
        video_description = request.POST.get('video_description')
        video_title = request.POST.get('video_title')
        video_id = request.POST.get('video_id')
        channel_title = request.POST.get('channel_title')
        video_date = request.POST.get('video_date')
        print("Video Date", video_date)
        d1 = datetime.datetime.strptime(video_date,"%Y-%m-%dT%H:%M:%SZ")
        channel_profile = request.POST.get('channel_profile')
        video_thumbnail_pic = request.POST.get('video_thumbnail_pic')
        print('VIdeo thumbnail*********', video_thumbnail_pic)
        WatchListobj= WatchList.objects.create(user= request.user, video_title=video_title, video_description=video_description, video_id=video_id,channel_title=channel_title, upload_date=video_date,channel_profile_pic=channel_profile,video_thumbnail_pic= video_thumbnail_pic)
        WatchListobj.save()
        print('****************************** Ajax Req', video_description)
    return HttpResponse('message')


def watch_list_view(request):
    try:
        print('Watch list view ****************************')
        all_videos= WatchList.objects.filter(user=request.user).order_by('-id')
        # ********************** Hero section background
        hero_section = HeroSection.objects.all().first() 
        context= {'all_videos': all_videos, 'hero_section':hero_section}
        return render(request, 'youtube/watch_list.html', context)
    except:
        return render(request, 'youtube/watch_list.html')

@csrf_exempt
def delete_watchlist_video(request):
    try:
        if request.method == 'POST':
            video_id= request.POST.get('video_id')
            video_obj= WatchList.objects.get(user= request.user, video_id= video_id)
            video_obj.delete()
        return HttpResponse('message')  
    except:
        return HttpResponse('Except message')

def channel_home_view(request):

    if request.method == 'POST':
        channel_id= request.POST.get('channel_id_home')
        print('*************** CHannel ID****************', channel_id)
        pl_request = youtube.playlists().list(
                part='snippet',
                channelId= channel_id,
        )
        video_request = youtube.search().list(
        part='snippet',
        type='video',
        channelId= channel_id,
        maxResults= 50
      ) 
        
        # To get the channel profile pic
        request_channel_snippet = youtube.channels().list(
            part='snippet, statistics',
            id=channel_id 
        )
        watchlist_videos= WatchList.objects.filter(user=request.user)
        videos_id_list=[]
        for video in watchlist_videos:
            videos_id_list.append(video.video_id)
        response_channel_snippet=request_channel_snippet.execute()
        channel_snippet_items= response_channel_snippet['items']
        channel_snippet_item= channel_snippet_items[0]
        # End profile picture
        print('channel_snippet_item+++++++++++++++++++++',response_channel_snippet)
        response = pl_request.execute()
        video_reponse= video_request.execute()
        pl_items= response['items']
        video_items= video_reponse['items']
        context= {'pl_items': pl_items, 'video_items': video_items, 'channel_item': channel_snippet_item, 'watchlist_videos': videos_id_list}
        print('Playlist ___', video_reponse)
        return render(request, 'youtube/channel_home.html', context)


def search_view(request):
    
    try:
        if request.method== 'POST':
            search_keyword= request.POST.get('search_keyword')
            keyword_obj= Keyword.objects.filter(keyword__icontains=search_keyword)
            if (keyword_obj.exists()):
                print('in if search')
                keyword= keyword_obj[0]
                keyword_var= keyword.keyword
                catgegory_var=keyword.category.category
                search_var= keyword_var+','+catgegory_var
                if keyword.channel_id:
                    print('Channel ID exist')
                    try:
                        video_request = youtube.search().list(
                        part='snippet',
                        type='video',
                        # q='Athletes,Football, Volleyball',
                        channelId= keyword.channel_id,
                        maxResults=50,
                        order= 'date'
                        
                    
                        )
                        video_response = video_request.execute()
                        video_items= video_response['items']
                    except:
                        video_request = youtube.search().list(
                                        part='snippet',
                                        type='video',
                                        q=search_var,
                                        maxResults=50,
                                        order= 'date' 
                            )
                        video_response = video_request.execute()
                        video_items= video_response['items']
                        # ******************* If search result did not return proper result
                        if len(video_items) < 10:
                            print('************** Len is less than 2s')
                            video_request = youtube.search().list(
                                part='snippet',
                                type='video',
                                q=keyword_var,
                                maxResults=50,
                                order= 'date' 
                            )
                            video_response = video_request.execute()
                            video_items= video_response['items']
                        if not len(video_items):
                            print('empty',video_items)
                            keyword_obj= keyword_obj[0]
                            video_items = keyword_obj.data
                        
                else:
                    video_request = youtube.search().list(
                            part='snippet',
                            type='video',
                            q=search_var,
                            maxResults=50,
                            order= 'date' 
                        )
                    video_response = video_request.execute()
                    video_items= video_response['items']
                    # ******************* If search result did not return proper result
                    if len(video_items) < 10:
                        print('************** Len is less than 2s')
                        video_request = youtube.search().list(
                            part='snippet',
                            type='video',
                            q=keyword_var,
                            maxResults=50,
                            order= 'date' 
                        )
                        video_response = video_request.execute()
                        video_items= video_response['items']
                    if not len(video_items):
                        print('empty',video_items)
                        keyword_obj= keyword_obj[0]
                        video_items = keyword_obj.data
                    
                watchlist_videos= WatchList.objects.filter(user=request.user)
                All_keywords= Keyword.objects.all()
                videos_id_list=[]
                for video in watchlist_videos:
                    videos_id_list.append(video.video_id)
                context= {'data': video_items, 'watchlist_videos': videos_id_list, 'all_keywords': All_keywords}
                return render(request, 'youtube/search.html', context)
            else:
                print('in else search')
                message= 'Sorry! No Search Result Found'
                context= {'message': message}
                return render(request, 'youtube/search.html', context)
    except Exception as e:
        print('except search', e)
        message= 'Sorry! No Search Result Found'
        context= {'data': "",'message': message}
        return render(request, 'youtube/search.html', context)
def auto_complete(request):
    
    All_keywords= Keyword.objects.all()
    keywords_list=list()
    for keyword in All_keywords:
        if keyword.keyword:
            if not keyword.disable:
                keywords_list.append(keyword.keyword)
    # print(keywords_list)   
    return JsonResponse({'data': keywords_list,})
    # return HttpResponse(json_list)






# Update data of the site in the database every 24 hour 

def update_data_db(request):
    api_key_6= 'AIzaSyAczxkO9D2vorvtomWQwtGLEnQ2FjmRdjk'
    youtube_db = build('youtube', 'v3', developerKey=api_key_6)
    all_keywords= Keyword.objects.all()

    blackListVideos = BlackListVideos.objects.all()
    blockVideoList = []
    blockChannelList = []
    for b in blackListVideos:
        blockVideoList.append(b.video_id)
        blockChannelList.append(b.channel_id)


    keyword_var=''
    data_list= []
    dummy_data_list=[]
    for keyword in all_keywords:
        keyword_var= keyword.keyword
        channel_id= keyword.channel_id
        catgegory_var=keyword.category.category 
        video_items=[]
        print('**************************')
        print(keyword_var, catgegory_var)
        
        try:
            if channel_id and channel_id not in blockChannelList:
                try:
                    print('*********Channel id api*******', channel_id)
                    video_request = youtube_db.search().list(
                        part='snippet',
                        type='video',
                        # q='Athletes,Football, Volleyball',
                        channelId= channel_id,
                        maxResults=50,
                        order= 'date'
                    )
                    video_response = video_request.execute()
                    video_items= video_response['items']
                    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                    # print('video Items', video_items)
                    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                    temp = video_items
                    temp2 = []
                    for video_data in temp:
                        if(video_data['id']['videoId'] not in blockVideoList):
                            temp2.append(video_data)

                    data_list = data_list+temp2
                    keyword.data=temp2
                    keyword.save()
                except:
                    try:
                        if keyword_var: 
                            search_var= keyword_var+','+catgegory_var
                            print('*********keyword api*******')   
                            print(search_var)
                            video_request = youtube.search().list(
                                part='snippet',
                                type='video',
                                # q='Athletes,Football, Volleyball',
                                q=search_var,
                                maxResults=50,
                                order= 'date'
                                
                            
                            )
                            video_response = video_request.execute()
                            video_items= video_response['items']
                            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                            # print('video Items', video_items)
                            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                            # ******************* If search result did not return proper result
                            if len(video_items) < 10:
                                print('************** Len is less than 2s')
                                video_request = youtube.search().list(
                                    part='snippet',
                                    type='video',
                                    q=keyword_var,
                                    maxResults=50,
                                    order= 'date' 
                                )
                                video_response = video_request.execute()
                                video_items= video_response['items']
                                print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                                # print('video Items', video_items)
                                print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                            temp = video_items
                            temp2 = []
                            for video_data in temp:
                                if(video_data['id']['videoId'] not in blockVideoList):
                                    temp2.append(video_data)
                            data_list = data_list+temp2
                            keyword.data=temp2
                            keyword.save()
                    except Exception as e1:

                        print('____________Except 1_____________________')
                        print('************Except 1**********************', )
                        print('except 1',e1)
                        api_key_6= 'AIzaSyAzaAIFiU2QKcD4sqC47j-I9-0fAk3awHw'
                        youtube_db = build('youtube', 'v3', developerKey=api_key_6)
                        
            
            else:
                    print('Else channel id not found')
                    try:
                        if keyword_var: 
                            search_var= keyword_var+','+catgegory_var
                            print('*********keyword api*******')   
                            print(search_var)
                            video_request = youtube_db.search().list(
                                part='snippet',
                                type='video',
                                # q='Athletes,Football, Volleyball',
                                q=search_var,
                                maxResults=50,
                                order= 'date'
                                
                            
                            )
                            video_response = video_request.execute()
                            video_items= video_response['items']
                            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                            # print('video Items', video_items)
                            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                            # ******************* If search result did not return proper result
                            if len(video_items) < 10:
                                print('************** Len is less than 2s')
                                video_request = youtube_db.search().list(
                                    part='snippet',
                                    type='video',
                                    q=keyword_var,
                                    maxResults=50,
                                    order= 'date' 
                                )
                                video_response = video_request.execute()
                                video_items= video_response['items']
                                print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                                # print('video Items', video_items)
                                print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                            temp = video_items
                            temp2 = []
                            for video_data in temp:
                                if(video_data['id']['videoId'] not in blockVideoList):
                                    temp2.append(video_data)
                            data_list = data_list+temp2
                            keyword.data=temp2
                            keyword.save()
                    except Exception as e1:
                        print('____________Except 1_____________________')
                        print('************Except 1**********************', )
                        print('except 1',e1)
                        api_key_6= 'AIzaSyAzaAIFiU2QKcD4sqC47j-I9-0fAk3awHw'
                        youtube_db = build('youtube', 'v3', developerKey=api_key_6)
                        
            
        except Exception as e2:
            print('except 2',e2)
            pass
        list=[]
        
        
        
        all_data_obj= AllData.objects.get(id=1)
        all_data_obj.data=data_list
        all_data_obj.save()
        
        print(keyword.data)
    return redirect('/watchlist')
        
@csrf_exempt
def filter_videos_home(request):
    try:
            videos_id_list_watchlist=[]
            watchlist_videos= WatchList.objects.filter(user=request.user)
            
            for video in watchlist_videos:
                videos_id_list_watchlist.append(video.video_id)
    except Exception as e:
            print(e)
            pass
    if request.method == 'POST':
        filter_category= request.POST.get('filter_category')
        filter= request.POST.get('filter')
        filter_type=type_of_filter(filter)
        print('category', filter_category)
        print('filter',filter)
        print('type_of_filter(filter)', type_of_filter(filter))
        # if filter == 'Default':
        #     first_data_list=[]
        #     follower_keyword_list=[]
        #     followed_obj= FollowPersonality.objects.filter(user=request.user,keyword__category__category=filter_category)
        #     if followed_obj.exists():
        #         for follower in followed_obj:
        #             first_data_list += follower.keyword.data
        #             follower_keyword_list.append(follower.keyword.keyword)

        #     keyword_obj= Keyword.objects.filter(category__category=filter_category).exclude(keyword__in=follower_keyword_list)
        #     for key in keyword_obj:
        #         first_data_list = first_data_list+ key.data
        #     sorted_list = first_data_list
        # else:
        All_keywords= Keyword.objects.filter(category__category = filter_category)
        keywords_data_list= []
        videos_api_data=[]
        keywords_string=""
        for keyword in All_keywords:
            try:
                if not keyword.disable:
                    keywords_data_list= keywords_data_list + (keyword.data)
            except:
                pass        
        video_id_list=[]
        for data in keywords_data_list:
            video_id=data['id']['videoId']

            # print('video id', video_id)
            # keywords_string=keywords_string+ ','+ str(video_id)
            # print(keywords_string)
            video_id_list.append(video_id)
        divided_chunk_list = list(divide_chunks(video_id_list, 50))
        for chunk in divided_chunk_list:
            keywords_string=''
            for val in chunk:
                keywords_string=keywords_string+ ','+ str(val)
                keywords_string=keywords_string.lstrip(',')
            request = youtube.videos().list(
                        part="statistics,snippet",
                        id=keywords_string,
                        maxResults=1
                        )
            response = request.execute()
            items= response['items']
            # print(items)
            videos_api_data= videos_api_data+items
        # keywords_string=keywords_string.lstrip(',')
        # print(type(keywords_string))
        # request = youtube.videos().list(
        # part="statistics,snippet",
        # id=keywords_string,
        # maxResults=1
        # )
        # response = request.execute()
        # items= response['items']
        # print('videos', videos_api_data)
        updated_data_list= []
        for item in videos_api_data:
            id=item['id']
            print('id',id)
            if item['statistics'].__contains__(str(filter_type)):
                updated_data_list.append(item)
                likes= item['statistics'][str(filter_type)]
                # print('likes', type(likes), likes)
        sorted_list=[]
        if filter == 'Default':
            sorted_list=sorted_list+videos_api_data
        else:    
            sorted_list=sorted(updated_data_list, key=lambda x: int(x['statistics'][str(filter_type)]), reverse=True)
        # print(sorted_list)  
        
    return JsonResponse({'data': sorted_list, 'videos_id_list':videos_id_list_watchlist})


# Follow a personality view
def follow_personality(request):
    try:
        all_keywords=Keyword.objects.filter(disable = False)
        all_followed_personality= FollowPersonality.objects.filter(user= request.user)
        followed_list=[]
        for personality in all_followed_personality:
            followed_list.append(personality.keyword.keyword)
        # ********************** Hero section background
        hero_section = HeroSection.objects.all().first() 
        context={'all_keywords': all_keywords,'followed_list': followed_list,'hero_section':hero_section}
        return render(request, 'youtube/personality_follow.html', context)
    except:
        return render(request, 'youtube/personality_follow.html')
# follow a personality AJAX
@ csrf_exempt
def follow_personality_ajax(request):
    if request.method == 'POST':
        follow_keyword=request.POST.get('follow_keyword')
        follow_keyword_channel_id= request.POST.get('follow_keyword_channel_id')
        print('follow', follow_keyword)
        print('unfollow', follow_keyword_channel_id)
        try:
            print('try')
            keyword_obj=Keyword.objects.get(keyword=follow_keyword)
            follow_personality_obj=FollowPersonality.objects.create(user=request.user, keyword=keyword_obj)
            follow_personality_obj.save()
        except:
            print('except')
            keyword_obj=Keyword.objects.get(channel_id=follow_keyword_channel_id)
            follow_personality_obj=FollowPersonality.objects.create(user=request.user, keyword=keyword_obj)
            follow_personality_obj.save()

    return HttpResponse('success')

# Unfollow a personality AJAX
@ csrf_exempt
def unfollow_personality_ajax(request):
    if request.method == 'POST':
        follow_keyword=request.POST.get('unfollow_keyword')
        unfollow_keyword_channel_id= request.POST.get('unfollow_keyword_channel_id')
        try:
            keyword_obj=Keyword.objects.get(keyword=follow_keyword)
            follow_personality_obj=FollowPersonality.objects.get(user=request.user, keyword=keyword_obj)
            follow_personality_obj.delete()
        except:
            keyword_obj=Keyword.objects.get(channel_id=unfollow_keyword_channel_id)
            follow_personality_obj=FollowPersonality.objects.get(user=request.user, keyword=keyword_obj)
            follow_personality_obj.delete()

    return HttpResponse('success')


def test(request):
    str_1=['w9HJw2eXyqE,MeMUO_D1-pg,YjJvlhF8d5c,6vjpHJMBcsI,wEI3zqxNKbw,n2lRTW2zwNc,uacpjGQLvuE,_92PIn1wj0k,HFnPL255muo,frhuuVWC0JY,FORzH8zSrtg']
    str_2=['w9HJw2eXyqE','MeMUO_D1-pg','YjJvlhF8d5c','6vjpHJMBcsI','wEI3zqxNKbw','n2lRTW2zwNc','uacpjGQLvuE','_92PIn1wj0k','HFnPL255muo','frhuuVWC0JY','FORzH8zSrtg']
    
    # print((str_2))
    n = 12
    # x=[]
    x = list(divide_chunks(str_2, n))
    for chunk in x:
        s=''
        for val in chunk:
            s=s+ ','+ str(val)
            s=s.lstrip(',')
            # print(str(val))
        # print('****************',s)
    # request = youtube.videos().list(
    #     part="statistics,snippet",
    #     id=str,
    #     maxResults=1
    # )
    # response = request.execute()
    # items= response['items']
    # for item in items:
    #     likes= item['statistics']['likeCount']
    #     print('likes', likes)
    # sorted_l=sorted(items, key=lambda x: x['statistics']['likeCount'])

    # print(x)
    # w=['Podcast']
    # w2=['Influencer', 'Athlete','Podcast', 'Competetion']
    # cat_obj_2= Category.objects.all().exclude(category__in=w2)
    # cat_obj= Category.objects.all().exclude(category__in=w)
    # matches = cat_obj_2 +cat_obj
    # print(type(matches))
    # for cat in matches:
    #     print(cat.category, type(cat))
    # keyword_obj= FollowPersonality.objects.get(keyword__keyword='Cole Sager')
    # pa_list= []
    # pa_list+= keyword_obj.keyword.data
            
    # paginator = Paginator(pa_list, 3)
    # page = request.GET.get('page', 1)
    # keywords = paginator.get_page(page)
    # for i in keywords:
    #     print(i)
    # print(keywords)
    all_keywords= Category.objects.all().order_by('order_of_display')
    
    # keyword_var=''
    # data_list= []
    # dummy_data_list=[]
    # for keyword in all_keywords:
    #     keyword_var= keyword.keyword
    #     channel_id= keyword.channel_id
    #     if keyword_var:
    #         print('Keyword', keyword_var)
    #     if channel_id:
    #         print('CHannel ID', channel_id)
    #         video_request = youtube.search().list(
    #             part='snippet',
    #             type='video',
    #             # q='Athletes,Football, Volleyball',
    #             channelId= channel_id,
    #             maxResults=30,
    #             order= 'date'
                
            
    #         )
    #         video_response = video_request.execute()
    #         video_items= video_response['items']
    #         keyword.data=video_items
    #         keyword.save()
    # most_recent_keywords= Keyword.objects.filter(most_recent=True)
    keyword = Keyword.objects.filter().first()
    data_list= keyword.data
    sorted_list=sorted(data_list, key=lambda x: (x['snippet']['publishedAt']), reverse=True)
    for dat in data_list:
        print('date', dat['snippet']['publishedAt']) 
    # for most_recent in most_recent_keywords:
    word = '2022 NOBULL CROSSFIT GAMES'
    string = 'Did my BIG RISKS Pay Off? // 2022 NOBULL CROSSFIT GAMES / Road to Madison'
    # for keyword in all_keywords:
        # print(keyword.category, keyword.id, keyword.order_of_display)    
    # context={'most_recent': most_recent_keywords}
    return render(request, 'youtube/personality_follow.html')


# All athletes Athletes Profile views
def all_profiles_view(request):
    # *********************** FOllowed athletes list

    # *******Athlete profiles which are being followed by  user
    followed_athletes= FollowedAthletes.objects.filter(user=request.user) 
    follow_athlete_list=[]
    # ********************* FOllowed athletes
    for athlete in followed_athletes:
        follow_athlete_list.append(athlete.followed_athlete.keyword.keyword)
    print('AThletes list', follow_athlete_list)

    all_profile_categories = AthleteProfileCategory.objects.all()

    all_athletes = AthleteProfile.objects.all()
    categories = Category.objects.all()
    context = {
        'all_athletes': all_athletes,
        'categories':categories,
        'followed_athletes_list':follow_athlete_list,
        'profile_categories':all_profile_categories
        }
    return render(request, 'youtube/athlete_profile/follow_athletes.html', context)

def athlete_profile(request):
    if request.method == 'POST':
        athlete_keyword = request.POST.get('athlete_keyword')
        print('Athlete Keyword', athlete_keyword)
        keyword_objects = Keyword.objects.filter(keyword = athlete_keyword )
        keyword_obj = keyword_objects[0]
        athlete = AthleteProfile.objects.filter(keyword = keyword_obj)
        # *********************** Saved videos list
   
        watchlist_videos= WatchList.objects.filter(user=request.user)
        videos_id_list=[]
        
        # ********************* Watch list videos
        for video in watchlist_videos:
            videos_id_list.append(video.video_id)
        print('Athlete', athlete)


        followed_athletes= FollowedAthletes.objects.filter(user=request.user)
        follow_athlete_list=[]
        
        # ********************* FOllowed athletes
        for followed_athlete in followed_athletes:
            follow_athlete_list.append(followed_athlete.followed_athlete.keyword.keyword)
        print('AThletes list', follow_athlete_list)


        context = {
            'athlete': athlete[0],
            'watchlist_videos_data': watchlist_videos,
            'followed_athletes_list':follow_athlete_list
        }
    return render(request, 'youtube/athlete_profile/athlete_profile.html', context)

def community(request):
    # *********************** FOllowed athletes list

    # *******Athlete profiles which are being followed by  user
    followed_athletes= FollowedCommunity.objects.filter(user=request.user) 
    follow_community_list=[]
    # ********************* FOllowed athletes
    for athlete in followed_athletes:
        follow_community_list.append(athlete.followed_community.keyword.keyword)
    print('AThletes list', follow_community_list)

    all_profile_categories = CommunityProfileCategory.objects.all()

    all_community = CommunityProfile.objects.all()
    categories = Category.objects.all()
    context = {
        'all_community': all_community,
        'categories':categories,
        'follow_community_list':follow_community_list,
        'profile_categories':all_profile_categories
        }
    return render(request, 'youtube/community/community.html', context)
def community_profile(request):
    if request.method == 'POST':
        community_keyword = request.POST.get('community_keyword')
        print('community_keyword Keyword', community_keyword)
        keyword_objects = Keyword.objects.filter(keyword = community_keyword )
        keyword_obj = keyword_objects[0]
        community = CommunityProfile.objects.filter(keyword = keyword_obj)
        # *********************** Saved videos list
   
        watchlist_videos= WatchList.objects.filter(user=request.user)
        videos_id_list=[]
        
        # ********************* Watch list videos
        for video in watchlist_videos:
            videos_id_list.append(video.video_id)
        print('Athlete', community)


        followed_communities= FollowedCommunity.objects.filter(user=request.user)
        follow_community_list=[]
        
        # ********************* FOllowed athletes
        for followed_community in followed_communities:
            follow_community_list.append(followed_community.followed_community.keyword.keyword)
        print('AThletes list', follow_community_list)


        context = {
            'community': community[0],
            'watchlist_videos_data': watchlist_videos,
            'follow_community_list':follow_community_list
        }
    return render(request, 'youtube/community/community_profile.html', context)

# Follow an athlete using AJAX
@csrf_exempt
def follow_athlete_ajax(request):
    if request.method == 'POST':
        follow_athlete_keyword=request.POST.get('follow_athlete_keyword')
        print('AJAX follow athlete keyword', follow_athlete_keyword)
        try:
            athlete_profile_obj = AthleteProfile.objects.filter(keyword__keyword=follow_athlete_keyword)
            follow_athlete_obj = FollowedAthletes.objects.create(user = request.user, followed_athlete = athlete_profile_obj[0])
            follow_athlete_obj.save()
        except:
            pass

    return HttpResponse('success')

# UNFollow an athlete using AJAX
@csrf_exempt
def unfollow_athlete_ajax(request):
    if request.method == 'POST':
        follow_athlete_keyword=request.POST.get('follow_athlete_keyword')
        print('AJAX unfollow athlete keyword ', follow_athlete_keyword)
        try:
            athlete_profile_obj = AthleteProfile.objects.filter(keyword__keyword=follow_athlete_keyword)
            follow_athlete_obj = FollowedAthletes.objects.filter(user = request.user, followed_athlete = athlete_profile_obj[0])
            follow_athlete_obj[0].delete()
        except Exception as e:
            print(e)
            

    return HttpResponse('success')



# Follow an community using AJAX
@csrf_exempt
def follow_community_ajax_call(request):
    if request.method == 'POST':
        follow_athlete_keyword=request.POST.get('follow_community_keyword')
        print('AJAX follow athlete keyword', follow_athlete_keyword)
        try:
            community_profile_obj = CommunityProfile.objects.filter(keyword__keyword=follow_athlete_keyword)
            
            print(community_profile_obj,"*************")

            follow_community_obj = FollowedCommunity.objects.create(user = request.user, followed_community = community_profile_obj[0])
            follow_community_obj.save()
        except:
            pass

    return HttpResponse('success')

# UNFollow an community using AJAX
@csrf_exempt
def unfollow_community_ajax_call(request):
    if request.method == 'POST':
        follow_athlete_keyword=request.POST.get('follow_community_keyword')
        print('AJAX unfollow athlete keyword ', follow_athlete_keyword)
        try:
            community_profile_obj = CommunityProfile.objects.filter(keyword__keyword=follow_athlete_keyword)
            follow_community_obj = FollowedCommunity.objects.filter(user = request.user, followed_community = community_profile_obj[0])
            follow_community_obj[0].delete()
        except Exception as e:
            print(e)
            

    return HttpResponse('success')

# ********************** Functions To use for different Operations
# Yield successive n-sized
# chunks from l.
def divide_chunks(l, n):
     
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

def type_of_filter(filter_key):
    if filter_key== 'Like' or filter_key== 'like' or filter_key== 'Likes' or filter_key== 'likes':
        returned_value='likeCount'
        return returned_value
    if filter_key== 'Comment' or filter_key== 'comment' or filter_key== 'Comments' or filter_key== 'comments':
        returned_value='commentCount'
        return returned_value
    if filter_key== 'View Count' or filter_key== 'view count':
        returned_value='viewCount'
        return returned_value
    if filter_key== 'View Count' or filter_key== 'view count':
        returned_value='viewCount'
        return returned_value

@login_required(login_url="login")
def block_video(request,id):
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print(id,"$$$$$$$$$$$$$$$$$$$$$$$")
    BlackListVideos.objects.create(video_id = id).save()
    return redirect('home')