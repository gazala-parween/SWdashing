require 'net/http'
require 'openssl'
require 'json'

SCHEDULER.every '5m', :first_in => 0 do |job|
  
  def video_stats(v_id)
	uri = URI("https://www.googleapis.com/youtube/v3/videos?part=statistics&id=
	"+v_id+"&key=AIzaSyBlRhNVLNqIO9UBBfw8HtV2MZkMeS0Y_q0")
    response = Net::HTTP.get(uri) # => String
    data = JSON.parse(response)
	return data['items'][0]['statistics']['viewCount']
  end


  

 def video_player(channelId)
 #print channelId
  uri=URI("https://www.googleapis.com/youtube/v3/search?part=snippet&channelId="+channelId+"&order=date&maxResults=5&key=AIzaSyBlRhNVLNqIO9UBBfw8HtV2MZkMeS0Y_q0")
  response = Net::HTTP.get(uri) # => String
  
  data = JSON.parse(response)

  
  youtube_videos = Array.new
	
  data['items'].each do |video|
      youtube_videos.push({
        label: video['snippet']['title'],
        value: video['id']['videoId'],
		value1:video_stats(video['id']['videoId'])
      })
   end   
  
 
  
  url_array = Array.new
  
   
  for each in youtube_videos do
	url = "http://www.youtube.com/embed/#{each[:value]}?autoplay=1"
	  
	url_array.push({
        :yurl => url,
		:title => each[:label],
		:count => each[:value1] 
        } )
  end
  #puts url_array
  return url_array
 end
 

 ch_id = ["UC1b6tyXZTHdIZ5vmgoAqn9w","UCx2HcmpB-UZGkMXOCJ4QIVA","UCNJcSUSzUeFm8W9P7UUlSeQ","UCzUYuC_9XdUUdrnyLii8WYg"]
 channel_arr = Array.new
 
 for ch_ in ch_id do
   channel_arr.push(video_player(ch_))
 end
 
 
#puts channel_arr

min=0
len=1  
arr = []
 
 for i in 0..4
	send_event('youtube_player1', { :items => channel_arr[0].slice(min, len) })
	send_event('youtube_player2', { :items => channel_arr[1].slice(min, len) })
	send_event('youtube_player3', { :items => channel_arr[2].slice(min, len) })
	send_event('youtube_player4', { :items => channel_arr[3].slice(min, len) })
    sleep(60)
    min=min+1    
 end

end