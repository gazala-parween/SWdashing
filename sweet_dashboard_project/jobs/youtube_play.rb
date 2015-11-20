require 'net/http'
require 'openssl'
require 'json'

# This job can track some metrics of a single youtube video by accessing the
# public available api of youtube.

# Config
# ------
youtube_api_key =  ENV['YOUTUBE_API_KEY'] || 'AIzaSyBlRhNVLNqIO9UBBfw8HtV2MZkMeS0Y_q0'
youtube_channel_id = ENV['YOUTUBE_CHANNEL_ID'] || 'UCx2HcmpB-UZGkMXOCJ4QIVA'
max_results = 50
# order the list by the numbers
ordered = true
max_length = 8

SCHEDULER.every '1m', :first_in => 0 do |job|
  http = Net::HTTP.new("www.googleapis.com", Net::HTTP.https_default_port())
  http.use_ssl = true
  http.verify_mode = OpenSSL::SSL::VERIFY_NONE # disable ssl certificate check
  response = http.request(Net::HTTP::Get.new("/youtube/v3/search?part=snippet&channelId=#{youtube_channel_id}&maxResults=#{max_results}&key=#{youtube_api_key}"))

  if response.code != "200"
    puts "youtube api error (status-code: #{response.code})\n#{response.body}"
  else
    data = JSON.parse(response.body, :symbolize_names => true)

    youtube_videos = Array.new

    data[:items].each do |video|
      youtube_videos.push({
    
        :value => video[:id][:videoId]
      })
    end
   end
	
   for each in youtube_videos do
	
	 it = "https://www.youtube.com/watch?v=#{each[:value]}"
	 it[.each do |v|
		url.push()
   end
	
	send_event('youtube_player', { items: url})
end