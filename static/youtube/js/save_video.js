$(".save_button").click(function(){
    var $this = $(this);
    $.ajax({ 
          method: "POST",
          url: `/addvideotowatchlist/`,
          data: {
        'video_description': $this.parent('div').siblings('.video_description').val(),
        'video_title': $this.parent('div').siblings('.video_title').val(),
        'video_id': $this.parent('div').siblings('.video_id').val(),
        'channel_title': $this.parent('div').siblings('.channel_title').val(),
        'video_date': $this.parent('div').siblings('.video_date').val(),
        'channel_profile': $this.parent('div').siblings('.channel_id').val(),
        'video_thumbnail_pic': $this.parent('div').siblings('.video_thumbnail_pic').val()
        
      },
          success:function(response){
            // $this.parent('div').html("<box-icon name='bookmark' type='solid' ></box-icon>")
            // $this.parent('div').html("<button type='button' class='unsave_button'><box-icon name='bookmark' type='solid' ></box-icon></button>")
            // $this.removeClass('save_button')
            // $this.addClass('unsave_button')
            $this.addClass('hidden')
            $this.siblings().removeClass('hidden')
            console.log('save response', response)
            
            
            
      
          },
          error:function(){
              console.log('save url is not working')
          }
        });
});
$(".unsave_button").click(function(){
    var $this = $(this);
    $.ajax({ 
          method: "POST",
          url: `/deletewatchlist/`,
          data: {
       
        'video_id': $this.parent('div').siblings('.video_id').val(),
      
        
      },
          success:function(response){
            // $this.html("<i class='bx bx-bookmark nav_icon'></i>")
            // $this.removeClass('unsave_button')
            // $this.addClass('save_button')
            // $this.parent('div').html("<button type='button' class='save_button'><i class='bx bx-bookmark nav_icon'></i></button>")
            $this.addClass('hidden')
            $this.siblings().removeClass('hidden')

            console.log('unsave response', response)
            
            
            
      
          },
          error:function(){
              console.log('unsave url is not working')
          }
        });
});


function save_video(save_element) {
    var $this = $(save_element);
    $.ajax({ 
          method: "POST",
          url: `/addvideotowatchlist/`,
          data: {
        'video_description': $this.parent('div').siblings('.video_description').val(),
        'video_title': $this.parent('div').siblings('.video_title').val(),
        'video_id': $this.parent('div').siblings('.video_id').val(),
        'channel_title': $this.parent('div').siblings('.channel_title').val(),
        'video_date': $this.parent('div').siblings('.video_date').val(),
        'channel_profile': $this.parent('div').siblings('.channel_id').val(),
        'video_thumbnail_pic': $this.parent('div').siblings('.video_thumbnail_pic').val()
        
      },
          success:function(response){
            // $this.parent('div').html("<box-icon name='bookmark' type='solid' ></box-icon>")
            // $this.parent('div').html("<button type='button' class='unsave_button'><box-icon name='bookmark' type='solid' ></box-icon></button>")
            // $this.removeClass('save_button')
            // $this.addClass('unsave_button')
            $this.addClass('hidden')
            $this.siblings().removeClass('hidden')
            console.log('save response', response)
            
            
            
      
          },
          error:function(){
              console.log('save url is not working')
          }
        });
  }

  function unsave_video(unsave_element) {
    var $this = $(unsave_element);
    $.ajax({ 
        method: "POST",
        url: `/deletewatchlist/`,
        data: {
     
      'video_id': $this.parent('div').siblings('.video_id').val(),
    
      
    },
        success:function(response){
          // $this.html("<i class='bx bx-bookmark nav_icon'></i>")
          // $this.removeClass('unsave_button')
          // $this.addClass('save_button')
          // $this.parent('div').html("<button type='button' class='save_button'><i class='bx bx-bookmark nav_icon'></i></button>")
          $this.addClass('hidden')
          $this.siblings().removeClass('hidden')

          console.log('unsave response', response)
          
          
          
    
        },
        error:function(){
            console.log('unsave url is not working')
        }
      });
  }


//   channel form submit

function channel_form_submit(channel_element) {
   
    $(channel_element).parent("form").submit()
  }

function video_form_submit(video_element){
    $(video_element).children('form').submit()
}
