require 'twitter'

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



SCHEDULER.every '1m', :first_in => 0 do |job|
  
    twee_arr =Array.new
    screen_name = ["@iamsrk","@chetan_bhagat","@narendramodi","@RashtrapatiBhvn"]
   for scr_ in screen_name
     tweets = twitter.user_timeline(scr_)
	
    if tweets
      tweets = tweets.map do |tweet|
        { name: tweet.user.name, count: tweet.retweet_count, body: tweet.text, avatar: tweet.user.profile_image_url_https }
      end
	end 
	
	twee_arr.push(tweets)
	#puts twee_arr
   end
   
      send_event('twitter_mentions1', comments: twee_arr[0])
      send_event('twitter_mentions2', comments: twee_arr[1])
	  send_event('twitter_mentions3', comments: twee_arr[2])
      send_event('twitter_mentions4', comments: twee_arr[3])
    
end