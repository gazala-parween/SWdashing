#!/usr/bin/python
# -*- coding: utf-8 -*-
import pymongo
import json
import time
import os
import subprocess
from bson import ObjectId
from pymongo import MongoClient
from shutil import copyfile



client = MongoClient('localhost', 27017)
db = client.dashing
collection = db.prefrences

def Login(uname):
    val=db.users.find_one({'username':uname})
    return str(val['_id'])
    
    

def Check(usr_, pass_):
    check_var = db.users.find({'username': usr_})
    for val_ in check_var:
        if val_['username'] == usr_ and val_['password'] == pass_:
            return True
        else:
            return False

def CreateUser(data_):
    usr=data_['username']
    pas=data_['password']
    perm=data_['permission']
    val=db.users.find_one({'username': usr})
    if val is None:
        db.users.insert({'username':usr,'password':pas,'permission':perm}) 
    val=db.users.find_one({'username':usr})
    return val

#    for v in val:
#        return v['_id'],v['username']

def CreateRecord(o_idR,u_nameR):
    val=db.prefrences.find_one({'_id': o_idR})
    if val is None:
        db.prefrences.insert({'user_id': o_idR,'username':u_nameR, 'reddit':[],'twitter':[],'youtube':[],'news':[]})
        
    
def CreateRubyDashboard(o_idD):

    content1="""
<% content_for :title do %>My super sweet dashboard<% end %>
    <div class="gridster">
        <ul>
        <li data-row="1" data-col="1" data-sizex="4" data-sizey="2">
        <div data-id='news"""+o_idD+"""' data-view="List3" data-title="NewsWhip" ></div>
        </li>
            <li data-row="2" data-col="1" data-sizex="2" data-sizey="1">
       <div data-id='twitter_mentions1"""+o_idD+"""' data-view="Comments" data-title="Tweets" style="background-color: #71388a"></div>
    </li>
	
	<li data-row="2" data-col="1" data-sizex="2" data-sizey="1">
       <div data-id='twitter_mentions2"""+o_idD+"""' data-view="Comments" data-title="Tweets" style="background-color: #71388a"></div>
    </li>
	
	<li data-row="2" data-col="1" data-sizex="2" data-sizey="1">
       <div data-id='twitter_mentions3"""+o_idD+"""' data-view="Comments" data-title="Tweets" style="background-color: #71388a"></div>
    </li>
	
	<li data-row="2" data-col="1" data-sizex="2" data-sizey="1">
       <div data-id='twitter_mentions4"""+o_idD+"""' data-view="Comments" data-title="Tweets" style="background-color: #71388a"></div>
    </li>
        <li data-row="1" data-col="1" data-sizex="4" data-sizey="1">
		<div data-id='reddit"""+o_idD+"""' data-view="Reddit" ></div>
	    </li>
            <li data-row="1" data-col="1" data-sizex="2" data-sizey="1" data-sizey="1">
        <div data-id='youtube_player1"""+o_idD+"""' data-view="Iframe" data-title="Channel: OYO" style="background-color: #c0392b"></div>
    </li>
	
	<li data-row="1" data-col="1" data-sizex="2" data-sizey="1" data-sizey="1">
        <div data-id='youtube_player2"""+o_idD+"""' data-view="Iframe" data-title="Channel: ScoopWhoop" style="background-color: #c0392b"></div>
    </li>
	
	<li data-row="1" data-col="1" data-sizex="2" data-sizey="1" data-sizey="1">
        <div data-id='youtube_player3"""+o_idD+"""' data-view="Iframe" data-title="Channel: TVF" style="background-color: #c0392b"></div>
    </li>
	
	<li data-row="1" data-col="1" data-sizex="2" data-sizey="1" data-sizey="1">
        <div data-id='youtube_player4"""+o_idD+"""' data-view="Iframe" data-title="Channel: AIB" style="background-color: #c0392b"></div>
    </li>
    </ul>
   </div> """

    
    file1= open("/Users/Yu/Documents/sweet_dashboard_project/dashboards/"+o_idD+".erb","wb+")
    file1.write(content1)
    file1.close()
    
    
def CreateRubyJob(o_idJ):
#    rus=username_
    content2=""" 
require 'net/http'
require 'json'
require 'twitter'
require 'openssl'

		

class Reddit
   
    def getTopPostsPerSubreddit()  
        #puts "hello"
    uri = URI('http://0.0.0.0:8080/api/?user_id="""+o_idJ+"""')
        response = Net::HTTP.get(uri)
        #puts response
        data = JSON.parse(response)
        #puts data
        subreddit =Array.new
    
        for d in data
            subreddit = d['reddit']
        end
        response = []
        posts = [];
        #print subreddit
        for it in subreddit
            #puts it
            url = URI("https://www.reddit.com"+it+"/.json")
            data = Net::HTTP.get(url)
            response = JSON.parse(data)
            
            items = []
            mastr_ar = response['data']['children']
            
            for item_ in mastr_ar[0..4]
                title = item_['data']['title']
                trimmed_title = title[0..85].gsub(/\s\w+$/, '...')
                items.push({
                    title: trimmed_title,
                    score: item_['data']['score'],
                    comments: item_['data']['num_comments']
                })
            end
            posts.push({ label: 'Current top posts in "' + it + '"', items: items })
        end
        
     posts
    end
end

@Reddit = Reddit.new();

SCHEDULER.every '20s', :first_in => 0 do |job|
  
  posts = @Reddit.getTopPostsPerSubreddit
    
  send_event('reddit"""+o_idJ+"""', { :posts => posts })
end		

#-----------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------

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

SCHEDULER.every '20s', :first_in => 0 do |job|

    uri = URI('http://0.0.0.0:8080/api/?user_id="""+o_idJ+"""')
    response = Net::HTTP.get(uri)
    data = JSON.parse(response)    

    handles =Array.new

    for d in data
        handles = d['twitter']
    end
    
    twee_arr =Array.new
    for h in handles
        tweets = twitter.user_timeline(h)
        if tweets
            tweets = tweets.map do |tweet|
                { name: tweet.user.name, count: tweet.retweet_count, body: tweet.text, avatar: tweet.user.profile_image_url_https }
                end
        end 
        twee_arr.push(tweets)
        #puts twee_arr
    end
   
      send_event('twitter_mentions1"""+o_idJ+"""', comments: twee_arr[0])
      send_event('twitter_mentions2"""+o_idJ+"""', comments: twee_arr[1])
	  send_event('twitter_mentions3"""+o_idJ+"""', comments: twee_arr[2])
      send_event('twitter_mentions4"""+o_idJ+"""', comments: twee_arr[3])
    
end


#-----------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------

		
SCHEDULER.every '20s', :first_in => 0 do |job|
  min = 0
  page_size= 5
    uri = URI('http://www.newswhip.com/api/v1/region/France/all/2?key=AHwaqz7hApx9D')
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
    send_event('news"""+o_idJ+"""', { items: newswhip_article.slice(min, page_size)})
	sleep(10)
	 
	min = min + page_size
        
  end
  
  send_event('news"""+o_idJ+"""', { items: newswhip_article.slice(min..max)})
	 
end

#-----------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------


SCHEDULER.every '20s', :first_in => 0 do |job|
  
  def video_stats(v_id)
	uri = URI("https://www.googleapis.com/youtube/v3/videos?part=statistics&id=
	"+v_id.to_s+"&key=AIzaSyBlRhNVLNqIO9UBBfw8HtV2MZkMeS0Y_q0")
    response = Net::HTTP.get(uri) # => String
    data = JSON.parse(response)
	return data['items'][0]['statistics']['viewCount']
  end


  puts "i m in yu"

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
	send_event('youtube_player1"""+o_idJ+"""', { :items => channel_arr[0].slice(min, len) })
	send_event('youtube_player2"""+o_idJ+"""', { :items => channel_arr[1].slice(min, len) })
	send_event('youtube_player3"""+o_idJ+"""', { :items => channel_arr[2].slice(min, len) })
	send_event('youtube_player4"""+o_idJ+"""', { :items => channel_arr[3].slice(min, len) })
    sleep(60)
    min=min+1    
 end

end


    """

    
    file2= open("/Users/Yu/Documents/sweet_dashboard_project/jobs/"+o_idJ+".rb","wb+")
    file2.write(content2)
    file2.close()

    
def Reddit(usr_r, text_r):
    val=db.prefrences.find({'user_id': usr_r})
    for v in val:
        var_ = v['reddit']
        if text_r in var_:
            return False
        else:
            collection.find_and_modify(query = {'user_id': usr_r}, update = {'$push':{ 'reddit': text_r}},upsert=True)
    
    
def Twitter(usr_t, text_t):
    val=db.prefrences.find({'user_id': usr_t})
    for v in val:
        var_ = v['twitter']
        if text_t in var_:
            return False
        else:
            collection.find_and_modify(query = {'user_id': usr_t}, update = {'$push':{ 'twitter': text_t}},upsert=True)
    
    
def Youtube(usr_y, text_y):
    val=db.prefrences.find({'user_id': usr_y})
    for v in val:
        var_ = v['youtube']
        if text_y in var_:
            return False
        else:
            collection.find_and_modify(query = {'user_id': usr_y}, update = {'$push':{ 'youtube': text_y}},upsert=True)
    
def News(usr_n, text_n):
    val=db.prefrences.find({'user_id': usr_n})
    for v in val:
        var_ = v['news']
        if text_n in var_:
            return False
        else:
            collection.find_and_modify(query = {'user_id': usr_n}, update = {'$push':{ 'news': text_n}},upsert=True)

    
def Api(id_):
#def Api():
    cursor = db.prefrences.find({'user_id': id_}) 
#    cursor = db.prefrences.find() 
    json_c = []
    for d in cursor:
        d['_id'] = str(d['_id'])
        dd = d
        json_c.append(dd)
    return json_c   
        
    
def RedditRemove(usr_rv,data_rv):
    val = collection.find_one({'user_id': usr_rv})
    red_var = val['reddit']
    for reddit in red_var:
        if reddit == data_rv:
            red_var.remove(reddit)
    collection.find_and_modify(query = {'user_id': usr_rv}, update = {'$set':{ 'reddit': red_var}},upsert=True)
    
    
def TwitterRemove(usr_tv,data_tv):
    val = collection.find_one({'user_id': usr_tv})
    tweet_var = val['twitter']
    for handles in tweet_var:
        if handles == data_tv:
            tweet_var.remove(handles)
    collection.find_and_modify(query = {'user_id': usr_tv}, update = {'$set':{ 'twitter': tweet_var}},upsert=True)
    
    
def YoutubeRemove(usr_yv,data_yv):
    val = collection.find_one({'user_id': usr_yv})
    you_var = val['youtube']
    for channel in you_var:
        if channel == data_yv:
            you_var.remove(channel)
    collection.find_and_modify(query = {'user_id': usr_yv}, update = {'$set':{ 'youtube': you_var}},upsert=True)
    

def NewsRemove(usr_nv,data_nv):
    val = collection.find_one({'user_id': usr_nv})
    news_var = val['news']
    for tags in news_var:
        if tags == data_nv:
            news_var.remove(tags)
    collection.find_and_modify(query = {'user_id': usr_nv}, update = {'$set':{ 'news': news_var}},upsert=True)
    
    
def Update():
    """os.chdir('sweet_dashboard_project')
    subprocess.call(["ls", "-l"])
    subprocess.call("dashing stop", shell=True)"""
    subprocess.call("bash /Users/Yu/dashing.sh", shell=True)
    
    
    
    
   

