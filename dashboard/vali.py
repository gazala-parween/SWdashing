#!/usr/bin/python
# -*- coding: utf-8 -*-
import pymongo
import json
import requests
import time
import os
import subprocess
from bson import ObjectId
from pymongo import MongoClient
from shutil import copyfile
import urllib
from whoosh.index import open_dir
from whoosh.query import Every
import petl as etl
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser


client = MongoClient('localhost', 27017)
db = client.dashing
collection = db.prefrences

def Login(uname):
    val=db.users.find_one({'username':uname})
    return val

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
        subprocess.call("bash /Users/Yu/dashing.sh", shell=True)
    val=db.users.find_one({'username':usr})
    return val

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
                <div data-id='news_"""+o_idD+"""' data-view="List3" data-title="Viral Stories" ></div>
            </li>
            
            <li data-row="2" data-col="1" data-sizex="2" data-sizey="1">
                <div data-id='twitter_mentions1_"""+o_idD+"""' data-view="Comments" data-title="Tweets" style="background-color: #71388a"></div>
            </li>
	
	          <li data-row="2" data-col="1" data-sizex="2" data-sizey="1">
                <div data-id='twitter_mentions2_"""+o_idD+"""' data-view="Comments" data-title="Tweets" style="background-color: #71388a"></div>
            </li>
	
	          <li data-row="2" data-col="1" data-sizex="2" data-sizey="1">
                <div data-id='twitter_mentions3_"""+o_idD+"""' data-view="Comments" data-title="Tweets" style="background-color: #71388a"></div>
            </li>
	
	          <li data-row="2" data-col="1" data-sizex="2" data-sizey="1">
                <div data-id='twitter_mentions4_"""+o_idD+"""' data-view="Comments" data-title="Tweets" style="background-color: #71388a"></div>
            </li>
            
            <li data-row="1" data-col="1" data-sizex="4" data-sizey="1">
		            <div data-id='reddit_"""+o_idD+"""' data-view="Reddit" ></div>
	          </li>
            
            <li data-row="1" data-col="1" data-sizex="2" data-sizey="1" data-sizey="1">
                <div data-id='youtube_player1_"""+o_idD+"""' data-view="Iframe" style="background-color: #c0392b"></div>
            </li>
	
	          <li data-row="1" data-col="1" data-sizex="2" data-sizey="1" data-sizey="1">
                <div data-id='youtube_player2_"""+o_idD+"""' data-view="Iframe" style="background-color: #c0392b"></div>
            </li>
	
	          <li data-row="1" data-col="1" data-sizex="2" data-sizey="1" data-sizey="1">
                <div data-id='youtube_player3_"""+o_idD+"""' data-view="Iframe" style="background-color: #c0392b"></div>
            </li>
	
	          <li data-row="1" data-col="1" data-sizex="2" data-sizey="1" data-sizey="1">
                <div data-id='youtube_player4_"""+o_idD+"""' data-view="Iframe" style="background-color: #c0392b"></div>
            </li>
      </ul>
   </div> """

    
    file1= open("/Users/Yu/Documents/sweet_dashboard_project/dashboards/"+o_idD+".erb","wb+")
    file1.write(content1)
    file1.close()
    
    
def CreateRubyJob(o_idJ):

    content2=""" 
require 'net/http'
require 'json'
require 'twitter'
require 'openssl'

SCHEDULER.every '1m', :first_in => 0 do |job|

  uri = URI('http://0.0.0.0:8080/api/?user_id="""+o_idJ+"""')
  response = Net::HTTP.get(uri)

  data = JSON.parse(response)

  subreddit =Array.new
    
  subreddit =  data[0]['reddit']
  puts subreddit
  response = []
  posts = [];
  if subreddit.length>0

        for it in subreddit
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
            puts items
            posts.push({ label: 'Current top posts in "' + it + '"', items: items })
            send_event('reddit_"""+o_idJ+"""', { :posts => posts })
        end
    end
end		

#--------------------------TWITTER---------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------


OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE
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
#if data.length>0
    handles =Array.new

    handles=data[0]['twitter']
    if handles.length>0
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
   
      send_event('twitter_mentions1_"""+o_idJ+"""', comments: twee_arr[0])
      send_event('twitter_mentions2_"""+o_idJ+"""', comments: twee_arr[1])
	  send_event('twitter_mentions3_"""+o_idJ+"""', comments: twee_arr[2])
      send_event('twitter_mentions4_"""+o_idJ+"""', comments: twee_arr[3])
    end
#end
end

#-----------------------------NEWSWHIP------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------



SCHEDULER.every '40s', :first_in => 0 do |job|
  	
  	min = 0
  	page_size= 5
    uri = URI('http://0.0.0.0:8080/whooshSearch/?user_id="""+o_idJ+"""')
    response = Net::HTTP.get(uri)
    data_n = JSON.parse(response)    
	
	if data_n.length>0
	    newswhip_article = Array.new
		for d in data_n
		
			newswhip_article.push({
                   	label: d['title'],
                	value: d['publisher'],
                    value2: d['count']})
        
		end

        max = newswhip_article.length
       	
       	while max > (min+page_size)
            send_event('news_"""+o_idJ+"""', { items: newswhip_article.slice(min, page_size)})
           	sleep(20)
            min = min + page_size
       end
            send_event('news_"""+o_idJ+"""', { items: newswhip_article.slice(min..max)})
    end
end
##----------------------------YOUTUBE-------------------------------------------------------------------------
##-------------------------------------------------------------------------------------------------------


SCHEDULER.every '5m', :first_in => 0 do |job|
    
uri = URI('http://0.0.0.0:8080/api/?user_id="""+o_idJ+"""')
response = Net::HTTP.get(uri)
data = JSON.parse(response)    
channel =Array.new
channel = data[0]['youtube']
    
def video_stats(v_id)
  uri = URI("https://www.googleapis.com/youtube/v3/videos?part=statistics&id="+v_id.to_s+"&key=AIzaSyBlRhNVLNqIO9UBBfw8HtV2MZkMeS0Y_q0")
  response = Net::HTTP.get(uri)
  data = JSON.parse(response)
  return data['items'][0]['statistics']['viewCount']
end


 def video_player(channelId)
     uri=URI("https://www.googleapis.com/youtube/v3/search?part=snippet&channelId="+channelId+"&order=date&maxResults=5&key=AIzaSyBlRhNVLNqIO9UBBfw8HtV2MZkMeS0Y_q0")
     response = Net::HTTP.get(uri)
     data = JSON.parse(response)
     youtube_videos = Array.new
    
     for item in data['items']
         if item['id']['videoId']!=nil
         data_ ={label: item['snippet']['title'],value: item['id']['videoId'],value1:video_stats(item['id']['videoId'])}
         youtube_videos.push(data_)
         end
     end   
    
     url_array = Array.new
     for each in youtube_videos do
         url = "http://www.youtube.com/embed/#{each[:value]}?autoplay=1"
         url_array.push({
             :yurl => url,
             :title => each[:label],
             :count => each[:value1] 
             })
     end
    return url_array
 end
    
if channel.length>0
    channel_arr = Array.new

    for ch_ in channel
      channel_arr.push(video_player(ch_))
    end
 
    min=0
    len=1
    k=1
    ch=channel_arr.length
     
    for i in 0..4
       for k in ch.times
         send_event('youtube_player'+(k+1).to_s+'_"""+o_idJ+"""', { :items => channel_arr[k].slice(min, len) })
         k=k+1
       end
       sleep(60)
       min=min+1
    end
    
end

end
    

    """

    
    file2= open("/Users/Yu/Documents/sweet_dashboard_project/jobs/"+o_idJ+".rb","wb+")
    file2.write(content2)
    file2.close()

    
def Reddit(usr_r, text_r):
    ur=urllib.urlopen('https://www.reddit.com'+text_r+'/.json')
    if ur.getcode() == 200:
        val=db.prefrences.find({'user_id': usr_r})
        for v in val:
            var_ = v['reddit']
            if text_r in var_:
                return False
            else:
                collection.find_and_modify(query = {'user_id': usr_r}, update = {'$push':{ 'reddit': text_r}},upsert=True)
                return True
    else:
        return False
    
def Twitter(usr_t, text_t):
    ur=urllib.urlopen('https://twitter.com/'+text_t)
    if ur.getcode() == 200:
        val=db.prefrences.find({'user_id': usr_t})
        for v in val:
            var_ = v['twitter']
            if text_t in var_:
                return False
            else:
                if len(var_)<4:
                    collection.find_and_modify(query = {'user_id': usr_t}, update = {'$push':{ 'twitter': text_t}},upsert=True)
                    return True
                else:
                    return False
    else:
        return False
    
def Youtube(usr_y, text_y):
    ur=urllib.urlopen('https://www.youtube.com/channel/'+text_y)
    if ur.getcode() == 200:
        val=db.prefrences.find({'user_id': usr_y})
        for v in val:
            var_ = v['youtube']
            if text_y in var_:
                return False
            else:
                if len(var_)<4:
                    collection.find_and_modify(query = {'user_id': usr_y}, update = {'$push':{ 'youtube': text_y}},upsert=True)
                    return True
                else:
                    return False
    else:
        return False
    
def News(usr_n, text_n):
    val=db.prefrences.find({'user_id': usr_n})
    for v in val:
        var_ = v['news']
        if text_n in var_:
            return False
        else:
            collection.find_and_modify(query = {'user_id': usr_n}, update = {'$push':{ 'news': text_n}},upsert=True)
            return True

    
def Api(id_):

    cursor = db.prefrences.find({'user_id': id_}) 
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
    
    
def Youtube_channelId_search(data_):
    video_id =data_
    req = requests.get("https://www.googleapis.com/youtube/v3/videos?id="+video_id+"&key=AIzaSyAeulKzsOmOn7-QYZeIpu3lDFTQI2PnUPI&part=snippet,contentDetails,statistics,status")
    data = json.loads(req.text)
#    print data
    for d in data['items']:
            channel_id = d['snippet']['channelId']
            channel_title = d['snippet']['channelTitle']
            return channel_id
    
    
#def Update():
#    """os.chdir('sweet_dashboard_project')
#    subprocess.call(["ls", "-l"])
#    subprocess.call("dashing stop", shell=True)"""
#    subprocess.call("bash /Users/Kumar/dashing.sh", shell=True)
    
def WhooshSearch(usr_w):
    val=db.prefrences.find_one({'user_id': usr_w})
    tags_=val['news']
    ix = open_dir('dashing.whoosh')
    ret_ar =[]
    with ix.searcher() as searcher:
        for t in tags_:
            query = MultifieldParser(["title","publisher","excerpt","keywords"], ix.schema).parse(unicode(t))
#            query = QueryParser("title", ix.schema).parse(unicode(t))
            results = searcher.search(query,limit=None)
            for result in results:
                obj = {"title":"","publisher":"","count":0}
                obj['title']= result['title']
                obj['count']= result['count']
                obj['publisher']= result['publisher']
                ret_ar.append(obj)
    return ret_ar

        
def UserApi():

    cursor = db.users.find() 
    json_c = []
    for d in cursor:
        d['_id'] = str(d['_id'])
        dd = d
        json_c.append(dd)
    return json.dumps(json_c) 
    
    
def UserRemove(usr_name):

    val2=collection.find_one({'username': usr_name})
    uid= val2['user_id']
    db.prefrences.remove({'user_id': uid})
    
    val=db.users.find_one({'username': usr_name})
    usrid= val['_id']
    db.users.remove({'_id': usrid})
    
    

#    
#    
#    subprocess.call("cd /Users/Yu/Documents/trash/")
#    subprocess.call("rm trycopy.py")
#    cd
#    cd /Users/Yu/Documents/gzl/
#    rm trycopy6.py
    
    
    
    
    
    
    
