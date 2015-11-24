#url = www.googleapis.com/youtube/v3/search?part=snippet&channelId=UCx2HcmpB-UZGkMXOCJ4QIVA&maxResults=5&key=AIzaSyBlRhNVLNqIO9UBBfw8HtV2MZkMeS0Y_q0

require 'net/http'
require 'openssl'
require 'json'

# This job can track some metrics of a single youtube video by accessing the
# public available api of youtube.

# Config
# ------
youtube_api_key =  ENV['YOUTUBE_API_KEY'] || 'AIzaSyBlRhNVLNqIO9UBBfw8HtV2MZkMeS0Y_q0'
youtube_channel_id = ENV['YOUTUBE_CHANNEL_ID'] || 'UCx2HcmpB-UZGkMXOCJ4QIVA' #'UCNJcSUSzUeFm8W9P7UUlSeQ'
max_results = 50
max_length = 8

#for each in youtube_channel_id do

SCHEDULER.every '20s', :first_in => 0 do |job|
  
  http = Net::HTTP.new("www.googleapis.com", Net::HTTP.https_default_port())
  http.use_ssl = true
  http.verify_mode = OpenSSL::SSL::VERIFY_NONE # disable ssl certificate check
  response = http.request(Net::HTTP::Get.new("/youtube/v3/search?part=snippet&channelId=#{youtube_channel_id}&maxResults=#{max_results}&order=date&key=#{youtube_api_key}"))
  
  
  if response.code != "200"
    puts "youtube api error (status-code: #{response.code})\n#{response.body}"
  else
    data = JSON.parse(response.body, :symbolize_names => true)
	
	youtube_videos = Array.new
	
    data[:items].each do |video|
      youtube_videos.push({
        label: video[:snippet][:title],
        value: video[:id][:videoId]
      })
    end
   
   
   #video_ar = []
   # puts data[:items]
   
   # for item in data[:items]
	# puts item,"  " 
   # end
   
   #puts youtube_videos
   
    youtube_stats = Array.new
    for each in youtube_videos do
      http = Net::HTTP.new("www.googleapis.com", Net::HTTP.https_default_port())
      http.use_ssl = true
      http.verify_mode = OpenSSL::SSL::VERIFY_NONE # disable ssl certificate check
      response = http.request(Net::HTTP::Get.new("/youtube/v3/videos?part=statistics&id=#{each[:value]}&key=#{youtube_api_key}"))
      data = JSON.parse(response.body, :symbolize_names => true)

      data[:items].each do |video|
        youtube_stats.push({
          label: each[:label],
		  value: each[:value],
          value1: video[:statistics][:viewCount].to_i
        })
      end
    end
	#def video_detil
	
   
 
 
   url_array = Array.new
   
   for each in youtube_stats do
	   
     url = "http://www.youtube.com/embed/#{each[:value]}?autoplay=1"
	  	
	   url_array.push({
          :yurl => url,
		  :title => each[:label],
		  :count => each[:value1]
        })
       end
     puts url_array
     
	 min=0
     len=1
 
     for each in url_array
	
          send_event('youtube_player', { :items => url_array.slice(min, len) })
  
          sleep(60)
          min=min+1
  
     end

	end
end