require 'net/http'
require 'json'
require 'twitter'
require 'openssl'

		

class Reddit
   
    def getTopPostsPerSubreddit()  
#        puts "hello05"
        uri = URI("http://0.0.0.0:8080/api/?user_id=56a376d1c44c2854565d7305")
        response = Net::HTTP.get(uri)
        #puts response
        data = JSON.parse(response)
        #puts data
        subreddit =Array.new
    
        for d in data
            subreddit = d['reddit']
        end
        response = []
        posts = [];
        #print subreddit
        for it in subreddit
            #puts it
            
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
        
     posts
    end
end

@Reddit = Reddit.new();

SCHEDULER.every '20s', :first_in => 0 do |job|
  
  posts = @Reddit.getTopPostsPerSubreddit
    
  send_event('reddit56a376d1c44c2854565d7305', { :posts => posts })
end		

#-----------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------

###ENV['SSL_CERT_FILE'] = File.expand_path('../cacert.pem', __FILE__)
OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE
#### Get your twitter keys & secrets:
#### https://dev.twitter.com/docs/auth/tokens-devtwittercom
twitter = Twitter::REST::Client.new do |config|
  config.consumer_key = 'Mqn1gEwkThO7puYnXQW8wJzEv'
  config.consumer_secret = 'p27JR9z378Ma9qbdhoRfPnI5ISnQUtFepMirzXhFGPyI9JuTHV'
  config.access_token = '3944171172-oGJ8S6DmDnqMc2uNwRtreVyxdTXFRQZcFVsENjY'
  config.access_token_secret = 'r9w7P4Ht0NQcHHL6Ni3PJv3EpOi2VbAsQcaDeVuagR0td'
end

SCHEDULER.every '20s', :first_in => 0 do |job|

    uri = URI("http://0.0.0.0:8080/api/?user_id=56a376d1c44c2854565d7305")
    response = Net::HTTP.get(uri)
    data = JSON.parse(response)    

    handles =Array.new

    for d in data
        handles = d['twitter']
    end
    
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
   
      send_event('twitter_mentions156a376d1c44c2854565d7305', comments: twee_arr[0])
      send_event('twitter_mentions256a376d1c44c2854565d7305', comments: twee_arr[1])
	  send_event('twitter_mentions356a376d1c44c2854565d7305', comments: twee_arr[2])
      send_event('twitter_mentions456a376d1c44c2854565d7305', comments: twee_arr[3])
    
end


#-----------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------

		
SCHEDULER.every '20s', :first_in => 0 do |job|
  min = 0
  page_size= 5
    uri = URI('http://www.newswhip.com/api/v1/region/France/all/2?key=AHwaqz7hApx9D')
  response = Net::HTTP.get(uri) # => String

  data = JSON.parse(response)

  newswhip_article = Array.new

  data['articles'].each do |arr|
    newswhip_article.push({
    label: arr['headline'],
	value: arr['source']['publisher'],
	value2: arr['fb_data']['like_count'] + arr['tw_data']['tw_count']})
  end
	
  max = newswhip_article.length
	
  while max > (min+page_size)
    send_event('news56a376d1c44c2854565d7305', { items: newswhip_article.slice(min, page_size)})
	sleep(10)
	 
	min = min + page_size
        
  end
  
  send_event('news56a376d1c44c2854565d7305', { items: newswhip_article.slice(min..max)})
	 
end

#-----------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------


#SCHEDULER.every '20s', :first_in => 0 do |job|
#  
#  def video_stats(v_id)
#	uri = URI("https://www.googleapis.com/youtube/v3/videos?part=statistics&id=
#	"+v_id.to_s+"&key=AIzaSyBlRhNVLNqIO9UBBfw8HtV2MZkMeS0Y_q0")
#    response = Net::HTTP.get(uri) # => String
#    data = JSON.parse(response)
#	return data['items'][0]['statistics']['viewCount']
#  end
#
#
#  puts "i m in yu"
#
# def video_player(channelId)
# #print channelId
#  uri=URI("https://www.googleapis.com/youtube/v3/search?part=snippet&channelId="+channelId+"&order=date&maxResults=5&key=AIzaSyBlRhNVLNqIO9UBBfw8HtV2MZkMeS0Y_q0")
#  response = Net::HTTP.get(uri) # => String
#  
#  data = JSON.parse(response)
#
#  
#  youtube_videos = Array.new
#	
#  data['items'].each do |video|
#      youtube_videos.push({
#        label: video['snippet']['title'],
#        value: video['id']['videoId'],
#		value1:video_stats(video['id']['videoId'])
#      })
#   end   
#  
# 
#  
#  url_array = Array.new
#  
#   
#  for each in youtube_videos do
#	url = "http://www.youtube.com/embed/#{each[:value]}?autoplay=1"
#	  
#	url_array.push({
#        :yurl => url,
#		:title => each[:label],
#		:count => each[:value1] 
#        } )
#  end
#  #puts url_array
#  return url_array
# end
# 
#
# ch_id = ["UC1b6tyXZTHdIZ5vmgoAqn9w","UCx2HcmpB-UZGkMXOCJ4QIVA","UCNJcSUSzUeFm8W9P7UUlSeQ","UCzUYuC_9XdUUdrnyLii8WYg"]
# channel_arr = Array.new
# 
# for ch_ in ch_id do
#   channel_arr.push(video_player(ch_))
# end
# 
# 
##puts channel_arr
#
#min=0
#len=1  
#arr = []
# 
# for i in 0..4
#	send_event('youtube_player156a376d1c44c2854565d7305', { :items => channel_arr[0].slice(min, len) })
#	send_event('youtube_player256a376d1c44c2854565d7305', { :items => channel_arr[1].slice(min, len) })
#	send_event('youtube_player356a376d1c44c2854565d7305', { :items => channel_arr[2].slice(min, len) })
#	send_event('youtube_player456a376d1c44c2854565d7305', { :items => channel_arr[3].slice(min, len) })
#    sleep(60)
#    min=min+1    
# end
#
#end
#
