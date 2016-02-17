 
require 'net/http'
require 'json'
require 'twitter'
require 'openssl'

SCHEDULER.every '1m', :first_in => 0 do |job|

  uri = URI('http://0.0.0.0:8080/api/?user_id=56b99553c44c2823254a026e')
  response = Net::HTTP.get(uri)

  data = JSON.parse(response)

  subreddit =Array.new
    
  subreddit =  data[0]['reddit']
  # puts subreddit
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
            # puts items
            posts.push({ label: 'Current top posts in "' + it + '"', items: items })
            send_event('reddit_56b99553c44c2823254a026e', { :posts => posts })
        end
    end
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

    uri = URI('http://0.0.0.0:8080/api/?user_id=56b99553c44c2823254a026e')
    response = Net::HTTP.get(uri)
    data = JSON.parse(response)    
#if data.length>0
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
   
      send_event('twitter_mentions1_56b99553c44c2823254a026e', comments: twee_arr[0])
      send_event('twitter_mentions2_56b99553c44c2823254a026e', comments: twee_arr[1])
	  send_event('twitter_mentions3_56b99553c44c2823254a026e', comments: twee_arr[2])
      send_event('twitter_mentions4_56b99553c44c2823254a026e', comments: twee_arr[3])
    end
#end
end

#-----------------------------NEWSWHIP------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------



SCHEDULER.every '40s', :first_in => 0 do |job|
  	
  	min = 0
  	page_size= 5
    uri = URI('http://0.0.0.0:8080/whooshSearch/?user_id=56b99553c44c2823254a026e')
    response = Net::HTTP.get(uri)
    data_n = JSON.parse(response)    
	
	if data_n.length>0
	    newswhip_article = Array.new
		for d in data_n
		
			newswhip_article.push({
                   	label: d['title'],
                	value: d['publisher'],
                    value2: d['count']})
        
		end

        max = newswhip_article.length
       	
       	while max > (min+page_size)
            send_event('news_56b99553c44c2823254a026e', { items: newswhip_article.slice(min, page_size)})
           	sleep(20)
            min = min + page_size
       end
            send_event('news_56b99553c44c2823254a026e', { items: newswhip_article.slice(min..max)})
    end
end
##----------------------------YOUTUBE-------------------------------------------------------------------------
##-------------------------------------------------------------------------------------------------------


SCHEDULER.every '5m', :first_in => 0 do |job|
    
uri = URI('http://0.0.0.0:8080/api/?user_id=56b99553c44c2823254a026e')
response = Net::HTTP.get(uri)
data = JSON.parse(response)    
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
    k=1
    ch=channel_arr.length
     
    for i in 0..4
       for k in ch.times
         send_event('youtube_player'+(k+1).to_s+'_56b99553c44c2823254a026e', { :items => channel_arr[k].slice(min, len) })
         k=k+1
       end
       sleep(60)
       min=min+1
    end
    
end

end
    

    