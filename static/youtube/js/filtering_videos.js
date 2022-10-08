$(".filter_dropdown_input").click(function(){
    var $this = $(this);
    var category_div=$this.siblings('#filter_category').val()
    $.ajax({ 
          method: "POST",
          url: `/filter_videos_home/`,
          data: {
        'filter_category': $this.siblings('#filter_category').val(),
        'filter': $this.text(),
       
        
      },
          success:function(response){
            $('.'+category_div).html("")
            html_var='<input type="text" hidden name="category_name" id="category_name" value="'+category_div+'">'

            $('.'+category_div).html(html_var)

            var keyword_data =response.data;
            var arrayLength = keyword_data.length; 
            for (var i = 0; i < arrayLength; i++) {
                    console.log('description',keyword_data[i].snippet.description)
                    console.log('Data'+String(i),keyword_data[i]);
                    var new_block= ' <div class="video_box"><div class="video_box_upper" onclick="video_form_submit(this)"><form action="{% url "video_player" %}" method="post">{% csrf_token %}<input  hidden name="video_description" value="'+keyword_data[i].snippet.description+'"><input hidden name="video_title" value="'+keyword_data[i].snippet.title+'"><input hidden name="video_id" value="'+keyword_data[i].id.videoId+'"><input hidden name="channel_title" value="'+keyword_data[i].snippet.channelTitle+'"><input hidden name="video_date" value="'+keyword_data[i].snippet.publishTime+'"><input hidden name="channel_id" value="'+keyword_data[i].snippet.channelId+'"></form><div style="margin-bottom: 5px;"><img src="'+keyword_data[i].snippet.thumbnails.high.url+'" alt="" width="100%"></div><div class="title_box"><p class="video_title">'+keyword_data[i].snippet.title+'</p> </div></div>  <div class="watch_list_block"><form action="{% url "channelhome" %}" method="post">{% csrf_token %}<input hidden class="channel_id" name="channel_id_home" value="'+keyword_data[i].snippet.channelId+'"><p onclick="channel_form_submit(this)" style="cursor: pointer;">'+keyword_data[i].snippet.channelTitle+'</p></form><input  hidden class="video_description" name="video_description" value="'+keyword_data[i].snippet.description+'"><input hidden class="video_title"  name="video_title" value="'+keyword_data[i].snippet.title+'"><input hidden class="video_id" name="video_id" value="'+keyword_data[i].id.videoId+'"><input hidden class="channel_title" name="channel_title" value="'+keyword_data[i].snippet.channelTitle+'"><input hidden class="video_date" name="video_date" value="'+keyword_data[i].snippet.publishedAt+'"><input hidden class="channel_id" name="channel_profile" value="'+keyword_data[i].snippet.channelId+'"><input hidden class="video_thumbnail_pic" name="video_thumbnail_pic" value="'+keyword_data[i].snippet.thumbnails.high.url+'"><div>{% if dat.id.videoId in watchlist_videos %}<button type="button" class="unsave_button  "  onclick="unsave_video(this)"><box-icon name="bookmark" color="white" type="solid" ></box-icon></button><button type="button"  class="save_button hidden"  onclick="save_video(this)"><i class="bx bx-bookmark bx-md nav_icon"></i></button>{% else %}<button type="button"  class="unsave_button hidden"  onclick="unsave_video(this)"><box-icon name="bookmark" color="white" type="solid" ></box-icon></button><button type="button" class="save_button" onclick="save_video(this)"><i class="bx bx-bookmark bx-md nav_icon"></i></button>{% endif %}</div></div>'

                    $this.append(new_block)
                    //Do something
                }
                            
            console.log('save response', response)
            
            
            
      
          },
          error:function(){
              console.log('save url is not working')
          }
        });
});