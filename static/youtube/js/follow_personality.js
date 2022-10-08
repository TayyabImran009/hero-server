function follow_personality(follow_element) {
    var $this = $(follow_element);
    $.ajax({ 
          method: "POST",
          url: `/follow_personality/`,
          data: {
        'follow_keyword': $this.parent('div').siblings('#follow_keyword_value').val(),
        'follow_keyword_channel_id': $this.parent('div').siblings('#follow_keyword_channel_id_value').val(),
      },
          success:function(response){
            // $this.parent('div').html("<box-icon name='bookmark' type='solid' ></box-icon>")
            // $this.parent('div').html("<button type='button' class='unsave_button'><box-icon name='bookmark' type='solid' ></box-icon></button>")
            // $this.removeClass('save_button')
            // $this.addClass('unsave_button')
            console.log('follow', $this.parent('div').siblings('#follow_keyword_channel_id_value').val())
            $this.addClass('hidden')
            $this.siblings().removeClass('hidden')
            console.log('follow response', response)
            
            
            
      
          },
          error:function(){
              console.log('save url is not working')
          }
        });
  }

function unfollow_personality(follow_element) {
    var $this = $(follow_element);
    $.ajax({ 
          method: "POST",
          url: `/unfollow_personality/`,
          data: {
        'unfollow_keyword': $this.parent('div').siblings('#follow_keyword_value').val(),
        'unfollow_keyword_channel_id': $this.parent('div').siblings('#follow_keyword_channel_id_value').val(),
      },
          success:function(response){
            // $this.parent('div').html("<box-icon name='bookmark' type='solid' ></box-icon>")
            // $this.parent('div').html("<button type='button' class='unsave_button'><box-icon name='bookmark' type='solid' ></box-icon></button>")
            // $this.removeClass('save_button')
            // $this.addClass('unsave_button')
            $this.addClass('hidden')
            $this.siblings().removeClass('hidden')
            console.log('unfollow response', response)
            
            
            
      
          },
          error:function(){
              console.log('save url is not working')
          }
        });
  }



