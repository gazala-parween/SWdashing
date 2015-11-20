require 'net/http'

require 'json'

min = 0
page_size= 5
#max_length = min + page_size
SCHEDULER.every '50s', :first_in => 0 do |job|
  uri = URI('http://www.newswhip.com/api/v1/region/India/all/6?key=AHwaqz7hApx9D')
  response = Net::HTTP.get(uri) # => String


  data = JSON.parse(response)

  newswhip_article = Array.new

  #newswhip_ar= []
  #i=0
  data['articles'].each do |arr|
      newswhip_article.push({
      label: arr['headline'],
	  value: arr['source']['publisher'],
	  #value2: arr['fb_data']['like_count'],
      value2: arr['fb_data']['like_count'] + arr['tw_data']['tw_count']})
	#if i<20
		#newswhip_ar << {:headline=>arr['headline'],:fb_like=>arr['fb_data']['like_count'],:tw_count=>arr['tw_data']['tw_count']}  
	#end
	#i+=1
	end
	max = newswhip_article.length
	#puts newswhip_ar
# :first_in sets how long it takes before the job is first run. In this case, it is run immediately
     while max > (min+page_size)
        send_event('news', { items: newswhip_article.slice(min, page_size)})
	   #puts min
		sleep(10)
	 
	    min = min + page_size
        #max = max + page_size
	 end
	 send_event('news', { items: newswhip_article.slice(min..max)})
	 
end
