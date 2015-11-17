require 'net/http'
require 'openssl'
require 'json'


SCHEDULER.every '1m', :first_in => 0 do |job|
  uri = URI('http://www.newswhip.com/api/v1/region/India/all/6?key=AHwaqz7hApx9D')
  response = Net::HTTP.get(uri) # => String


  data = JSON.parse(response.body, :symbolize_names => true)

  newswhip_article = Array.new

  data[:articles].each do |arr|
     newswhip_article.push({
     label: arr[:headline],
	 value: arr[:fb_data][:like_count],
     value2: arr[:tw_data][:tw_count]

# :first_in sets how long it takes before the job is first run. In this case, it is run immediately

   send_event('newswhip_views', {articles: newswhip_article})
end