require 'net/http'
require 'json'
require 'twitter'
require 'openssl'

		
def getTopPostsPerSubreddit()  

    uri = URI('http://0.0.0.0:8080/api/?user_id=56b83edebf5f1e460985b5a1')
    response = Net::HTTP.get(uri)
    
    data = JSON.parse(response)

    subreddit =Array.new
    
    subreddit =  data[0]['reddit']
    response = []
    posts = [];
   if subreddit.length>0

        for it in subreddit
            url = URI("https://www.reddit.com"+it+"/.json")
            data = Net::HTTP.get(url)
            response = JSON.parse(data)

            items = []
            mastr_ar = response['data']['children']

            for item_ in mastr_ar[0..4]
                title = item_['data']['title']
                trimmed_title = title[0..85].gsub(/\s\w+$/, '...')
                items.push({
                    title: trimmed_title,
                    score: item_['data']['score'],
                    comments: item_['data']['num_comments']
                })
            end
            posts.push({ label: 'Current top posts in "' + it + '"', items: items })
        end
   end  
    return posts
end



SCHEDULER.every '20s', :first_in => 0 do |job|
  posts = getTopPostsPerSubreddit
    
  send_event('reddit_56b83edebf5f1e460985b5a1', { :posts => posts })
end		

#--------------------------TWITTER---------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------


OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE
twitter = Twitter::REST::Client.new do |config|
  config.consumer_key = 'Mqn1gEwkThO7puYnXQW8wJzEv'
  config.consumer_secret = 'p27JR9z378Ma9qbdhoRfPnI5ISnQUtFepMirzXhFGPyI9JuTHV'
  config.access_token = '3944171172-oGJ8S6DmDnqMc2uNwRtreVyxdTXFRQZcFVsENjY'
  config.access_token_secret = 'r9w7P4Ht0NQcHHL6Ni3PJv3EpOi2VbAsQcaDeVuagR0td'
end

SCHEDULER.every '20s', :first_in => 0 do |job|
    
    uri = URI('http://0.0.0.0:8080/api/?user_id=56b83edebf5f1e460985b5a1')
    response = Net::HTTP.get(uri)
    data = JSON.parse(response)   
    
if data.length>0
    handles =Array.new

    handles=data[0]['twitter']
    
    if handles.length>0
    twee_arr =Array.new
    for h in handles
        tweets = twitter.user_timeline(h)
        if tweets
            tweets = tweets.map do |tweet|
                { name: tweet.user.name, count: tweet.retweet_count, body: tweet.text, avatar: tweet.user.profile_image_url_https }
                end
        end 
        twee_arr.push(tweets)
        #puts twee_arr
    end
   
      send_event('twitter_mentions1_56b83edebf5f1e460985b5a1', comments: twee_arr[0])
      send_event('twitter_mentions2_56b83edebf5f1e460985b5a1', comments: twee_arr[1])
	  send_event('twitter_mentions3_56b83edebf5f1e460985b5a1', comments: twee_arr[2])
      send_event('twitter_mentions4_56b83edebf5f1e460985b5a1', comments: twee_arr[3])
    end
end
end

#-----------------------------NEWSWHIP------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------


SCHEDULER.every '20s', :first_in => 0 do |job|
  min = 0
  page_size= 5
    uri = URI('http://0.0.0.0:8080/api/?user_id=56b83edebf5f1e460985b5a1')
    response = Net::HTTP.get(uri)
    data = JSON.parse(response)    
if data.length>0
    tags =Array.new
    tags = data[0]['news']
    
    if tags.length>0
        
        for t in tags do
            uri = URI('https://api.newswhip.com/v1/search?q='+t+'&key=AHwaqz7hApx9D')
            response = Net::HTTP.get(uri)
            data = JSON.parse(response)
            newswhip_article = Array.new

            data['articles'].each do |arr|
                newswhip_article.push({
                    label: arr['headline'],
                    value: arr['source']['publisher'],
                    value2: arr['fb_data']['like_count'] + arr['tw_data']['tw_count']})
                end
        end

        max = newswhip_article.length
        while max > (min+page_size)
            send_event('news_56b83edebf5f1e460985b5a1', { items: newswhip_article.slice(min, page_size)})
            sleep(10)
            min = min + page_size
        end
        send_event('news_56b83edebf5f1e460985b5a1', { items: newswhip_article.slice(min..max)})
    end
end
end


##----------------------------YOUTUBE-------------------------------------------------------------------------
##-------------------------------------------------------------------------------------------------------
#
#
SCHEDULER.every '2m', :first_in => 0 do |job|
    
uri = URI('http://0.0.0.0:8080/api/?user_id=56b83edebf5f1e460985b5a1')
response = Net::HTTP.get(uri)
data = JSON.parse(response)
    if data.length>0
channel =Array.new
channel = data[0]['youtube']
    
def video_stats(v_id)
  uri = URI("https://www.googleapis.com/youtube/v3/videos?part=statistics&id="+v_id.to_s+"&key=AIzaSyBlRhNVLNqIO9UBBfw8HtV2MZkMeS0Y_q0")
  response = Net::HTTP.get(uri)
  data = JSON.parse(response)
  return data['items'][0]['statistics']['viewCount']
end


 def video_player(channelId)
     uri=URI("https://www.googleapis.com/youtube/v3/search?part=snippet&channelId="+channelId+"&order=date&maxResults=5&key=AIzaSyBlRhNVLNqIO9UBBfw8HtV2MZkMeS0Y_q0")
     response = Net::HTTP.get(uri)
     data = JSON.parse(response)
     youtube_videos = Array.new
    
     for item in data['items']
         if item['id']['videoId']!=nil
         data_ ={label: item['snippet']['title'],value: item['id']['videoId'],value1:video_stats(item['id']['videoId'])}
         youtube_videos.push(data_)
         end
     end   
    
     url_array = Array.new
     for each in youtube_videos do
         url = "http://www.youtube.com/embed/#{each[:value]}?autoplay=1"
         url_array.push({
             :yurl => url,
             :title => each[:label],
             :count => each[:value1] 
             })
     end
    return url_array
 end
    
if channel.length>0
channel_arr = Array.new
for ch_ in channel
    channel_arr.push(video_player(ch_))
 end
 
min=0
len=1  
arr = []
    k=0
    for i in channel_arr[0..5]
        send_event('youtube_player'+(k+1).to_s+'_56b83edebf5f1e460985b5a1', { :items => i.slice(min, len) })
        k+=1
        sleep(60)
        min=min+1  
    end    
    
end
end


    
end
    