# This job displays all the newswhip articles of region india from last 2hrs 5 at a time by accessing the public available api of newswhip.

require 'net/http'
require 'json'

min = 0
page_size= 5

# :first_in sets how long it takes before the job is first run. In this case, it is run immediately

SCHEDULER.every '10s', :first_in => 0 do |job|
  uri = URI('http://www.newswhip.com/api/v1/region/India/all/2?key=AHwaqz7hApx9D')
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
    send_event('news', { items: newswhip_article.slice(min, page_size)})
	sleep(10)
	 
	min = min + page_size
        
  end
  
  send_event('news', { items: newswhip_article.slice(min..max)})
	 
end
