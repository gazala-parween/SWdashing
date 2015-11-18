require 'net/http'

require 'json'

max_length = 10
SCHEDULER.every '1m', :first_in => 0 do |job|
  uri = URI('http://www.newswhip.com/api/v1/region/India/all/1?key=AHwaqz7hApx9D')
  response = Net::HTTP.get(uri) # => String


  data = JSON.parse(response)

  newswhip_article = Array.new

  #newswhip_ar= []
  #i=0
  data['articles'].each do |arr|
      newswhip_article.push({
      label: arr['headline'],
	  value: arr['fb_data']['like_count'],
      value2: arr['tw_data']['tw_count']})
	#if i<20
		#newswhip_ar << {:headline=>arr['headline'],:fb_like=>arr['fb_data']['like_count'],:tw_count=>arr['tw_data']['tw_count']}  
	#end
	#i+=1
	end
	#puts newswhip_ar
# :first_in sets how long it takes before the job is first run. In this case, it is run immediately
   
     send_event('news', { items: newswhip_article.slice(0, max_length)})
	
end
