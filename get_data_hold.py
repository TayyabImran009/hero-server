from googleapiclient.discovery import build
import schedule
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Youtube_api.settings")
import django
django.setup()
from youtube_app.models import *
from users_data.models import*

from datetime import datetime


# Youtube API Key
api_key= 'AIzaSyAzaAIFiU2QKcD4sqC47j-I9-0fAk3awHw'
api_key_2='AIzaSyAo9njxj8OJpWshmpCyamYf9GJXN-kIi64'
api_key_3='AIzaSyBztkmRfxkYWS9QCtS9XD8r6clecRBVK2s'
api_key_4='AIzaSyA4Mt5QJqtcTJ77BHIeFAj12M6s5mSUiFQ'
api_key_5='AIzaSyA6aQiZykCZBYzGheYaKYdJYPKUsAQrrCs'
api_key_6= 'AIzaSyAczxkO9D2vorvtomWQwtGLEnQ2FjmRdjk'


youtube = build('youtube', 'v3', developerKey=api_key_2)

def update_data_db():
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


schedule.every().day.at("07:00").do(update_data_db)
  
while True:
    schedule.run_pending()

