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

  uri=URI('https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=UCx2HcmpB-UZGkMXOCJ4QIVA&order=date&maxResults=5&key=AIzaSyBlRhNVLNqIO9UBBfw8HtV2MZkMeS0Y_q0')
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
   
  #puts youtube_videos
  
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
  
  min=0
  len=1  
  for each in url_array
	send_event('youtube_player', { :items => url_array.slice(min, len) })
    sleep(60)
    min=min+1    
  end
end
