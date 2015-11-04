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

screen_name = URI::encode('@chetan_bhagat')

SCHEDULER.every '1m', :first_in => 0 do |job|
  ##begin
    tweets = twitter.user_timeline('@chetan_bhagat')

    if tweets
      tweets = tweets.map do |tweet|
        { name: tweet.user.name, body: tweet.text, avatar: tweet.user.profile_image_url_https }
      end
      send_event('twitter_mentions', comments: tweets)
    end
  ##rescue Twitter::Error
  ##  puts "\e[33mFor the twitter widget to work, you need to put in your twitter API keys in the jobs/twitter.rb file.\e[0m"
  ##end
end