$(document).ready(function () {
    window.localStorage.setItem("username","");
    loadcontent();
    function loadcontent(){
            $.ajax({
            url: 'http://0.0.0.0:8080/api/',
            data:{"user_id":window.localStorage.getItem("user_id")},
            error: function (e) {console.log(e.error);},
            success: function (data) {
                showcontent(data);
                console.log(data);
            },
            type: 'GET',dataType:'json'
        });
    };
    

    
    function showcontent(j_data){
        

        console.log(j_data.length);
        var  data = j_data[0];
 
        
        var reddit_str = "";
        for(i=0;i<data['reddit'].length;i++)
        {
            reddit_str +='<p class="reddit_del">'+data['reddit'][i]+'</p>' 
        }
        $("#reddit_container").html(reddit_str);
        
        var twitter_str = "";
        for(i=0;i<data['twitter'].length;i++)
        {
            twitter_str +='<p class="twitter_del">'+data['twitter'][i]+'</p>' 
        }
        $("#twitter_container").html(twitter_str);
        
        var youtube_str = "";
//        console.log(data['youtube']);
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
            },
            type: 'GET'
        });
        
    });
    
    $("#redditBtn").click(function(){ console.log("reddit");
        $.ajax({
            url: 'http://0.0.0.0:8080/reddit/',
            data:{redditText:$( "#redditText" ).val()},
            error: function (e) {console.log(e.error);},
            success: function (data) {
            },
            type: 'POST'
        });
        
    });
    
    
    $("#twitterBtn").click(function(){ console.log("twitter");
        $.ajax({
            url: 'http://0.0.0.0:8080/twitter/',
            data:{twitterText:$( "#twitterText" ).val()},
            error: function (e) {console.log(e.error);},
            success: function (data) {
            },
            type: 'POST'
        });
        
    })
    
    

    $("#youtubeBtn").click(function(){ console.log("youtube");
        $.ajax({
            url: 'http://0.0.0.0:8080/youtube/',
            data:{youtubeText:$( "#youtubeText" ).val()},
            error: function (e) {console.log(e.error);},
            success: function (data) {
            },
            type: 'POST'
        });
        
    })
    
    $("#newsBtn").click (function(){ console.log("news");
        $.ajax({
            url: 'http://0.0.0.0:8080/news/',
            data:{newsText:$( "#newsText" ).val()},
            error: function (e) {console.log(e.error);},
            success: function (data) {
            },
            type: 'POST'
        });
        
    })
});


