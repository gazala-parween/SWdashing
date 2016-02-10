$(document).ready(function () {
    window.localStorage.setItem("username","");
    console.log(curPage);
   
    if (curPage==="editPrefrences"){
        loadcontent();
    }
    else if(curPage==="createUser"){
        loaduserdetails();
    }
    
    function loadcontent(){
            $.ajax({
            url: 'http://0.0.0.0:8080/api/',
            data:{"user_id":window.localStorage.getItem("user_id")},
            error: function (e) {console.log(e.error);},
            success: function (data) {
                showcontent(data);
                console.log("loadData");
                console.log(data);
            },
            type: 'GET',dataType:'json'
        });
    };
    
    function loaduserdetails(){
            $.ajax({
            url: 'http://0.0.0.0:8080/userApi/',
            error: function (e) {console.log(e.error);},
            success: function (data) {
                showuser(JSON.parse(data));
                console.log(JSON.parse(data));
            },
            type: 'GET',dataType:'html',
        });
    };
    
    function showuser(u_data){
    
    var user_str = "";
        console.log(u_data)
        for(i=0;i<u_data.length;i++)
        {
//            console.log(u_data[i])
      user_str += '<p class="user_del">'+u_data[i].username+'</p>';
        
        }
        $("#user_container").html(user_str);
        
        
          $(".user_del").click(function(){
        console.log($(this).text());
                $.ajax({
            url: 'http://0.0.0.0:8080/userRemove/',
            data:{userRem:$(this).text()},
            error: function (e) {console.log(e.error);},
            success: function (data) {
                loaduserdetails();
            },
            type: 'POST'
                    }); 
            });
    }
    
    function showcontent(j_data){

        console.log(j_data.length);
        var  data = j_data[0];
 
        
        var reddit_str = "";
        for(i=0;i<data['reddit'].length;i++)
        {
            reddit_str +='<p class="reddit_del">'+data['reddit'][i]+'<img src="../images/Deletion_icon.png" width="15" height="15"></p>' 
        }
        $("#reddit_container").html(reddit_str);
        
        var twitter_str = "";
        for(i=0;i<data['twitter'].length;i++)
        {
            twitter_str +='<p class="twitter_del">'+data['twitter'][i]+'</p>' 
        }
        $("#twitter_container").html(twitter_str);
        
        var youtube_str = "";

        for(i=0;i<data['youtube'].length;i++)
        {
            youtube_str +='<p class="youtube_del">'+data['youtube'][i]+'</p>' 
        }
        $("#youtube_container").html(youtube_str);
        
        var news_str = "";
        for(i=0;i<data['news'].length;i++)
        {
            news_str +='<p class="news_del">'+data['news'][i]+'</p>' 
        }
        $("#news_container").html(news_str);
        
        
       
            $(".reddit_del").click(function(){
        console.log($(this).text());
                $.ajax({
            url: 'http://0.0.0.0:8080/redditRemove/',
            data:{redditRem:$(this).text()},
            error: function (e) {console.log(e.error);},
            success: function (data) {
                loadcontent();
            },
            type: 'POST'
                    }); 
            });
        
          $(".twitter_del").click(function(){
        console.log($(this).text());
                $.ajax({
            url: 'http://0.0.0.0:8080/twitterRemove/',
            data:{twitterRem:$(this).text()},
            error: function (e) {console.log(e.error);},
            success: function (data) {
                loadcontent();
            },
            type: 'POST'
                    }); 
            });
        
        $(".youtube_del").click(function(){
        console.log($(this).text());
                $.ajax({
            url: 'http://0.0.0.0:8080/youtubeRemove/',
            data:{youtubeRem:$(this).text()},
            error: function (e) {console.log(e.error);},
            success: function (data) {
                loadcontent();
            },
            type: 'POST'
                    }); 
            });
        
        $(".news_del").click(function(){
        console.log($(this).text());
                $.ajax({
            url: 'http://0.0.0.0:8080/newsRemove/',
            data:{newsRem:$(this).text()},
            error: function (e) {console.log(e.error);},
            success: function (data) {
                loadcontent();
            },
            type: 'POST'
                    }); 
            });
   } 
    
    
   $("#updateBtn").click(function(){ console.log("update");
        $.ajax({
            url: 'http://0.0.0.0:8080/update/',
    
            error: function (e) {console.log(e.error);},
            success: function (data) {
                console.log("updated data");
            },
            type: 'GET'
        });
        
    });

    $("#redditBtn").on("click",function(){
    $.ajax({
            url: 'http://0.0.0.0:8080/reddit/',
            data:{redditText:$( "#redditText" ).val()},
            dataType: 'html',
            success: function (data) {
                console.log(data);
                var someData = JSON.parse(data);                
                console.log(data,someData);
                if (someData.status){
                    $("#reddit_container").append('<p class="reddit_del">'+$( "#redditText" ).val()+'</p>');
                    $( "#redditText" ).val('');
                }
                else{
                    $("#redditError").show();
                }
            },
            error: function (e) {
                $("#redditError").show();
                console.log(e);
                
            },            
            type: 'POST'
        });
        
    })
    
    $("#twitterBtn").click(function(){ console.log("twitter");
        $.ajax({
            url: 'http://0.0.0.0:8080/twitter/',
            data:{twitterText:$( "#twitterText" ).val()},
            dataType: 'html',
            success: function (data) {
                console.log(data);
                var someData = JSON.parse(data);                
                console.log(data,someData);
                if (someData.status){
                    $("#twitter_container").append('<p class="reddit_del">'+$( "#twitterText" ).val()+'</p>');
                    $( "#twitterText" ).val('');
                }
                else{
                    $("#twitterError").show();
                } 
            },
            error: function (e) {
                $("#twitterError").show();
                console.log(e);
            },            
            type: 'POST'
    
        });
        
    })
    
    

    $("#youtubeBtn").click(function(){ console.log("youtube");
        $.ajax({
            url: 'http://0.0.0.0:8080/youtube/',
            data:{youtubeText:$( "#youtubeText" ).val()},
            dataType: 'html',
            success: function (data) {
                console.log(data);
                var someData = JSON.parse(data);                
                console.log(data,someData);
                if (someData.status){
                    $("#youtube_container").append('<p class="reddit_del">'+$( "#youtubeText" ).val()+'</p>');
                    $( "#youtubeText" ).val('');
                }
                    
            },
            error: function (e) {
                console.log(e);
                
            }, 
            type: 'POST'
        });
        
    })
    
    $("#newsBtn").click (function(){ console.log("news");
        $.ajax({
            url: 'http://0.0.0.0:8080/news/',
            data:{newsText:$( "#newsText" ).val()},
            dataType: 'html',
            success: function (data) {
                console.log(data);
                var someData = JSON.parse(data);                
                console.log(data,someData);
                if (someData.status){
                    $("#news_container").append('<p class="reddit_del">'+$( "#newsText" ).val()+'</p>');
                    $( "#newsText" ).val('');
                }
                  
            },
            type: 'POST'
        });
        
    })
    
    $("#searchBtn").click (function(){
        
        console.log("search_channelId");
        $.ajax({
            url: 'http://0.0.0.0:8080/youtubeChannelId/',
            data:{searchText:$( "#searchText" ).val()},
            error: function (e) {console.log(e.error);},
            success: function (data) {
                $("#cid").html(data);
            },
            type: 'GET'
        });
    })
});


