#!/usr/bin/python
# -*- coding: utf-8 -*-
import pymongo
import json
import time
import os
import subprocess
from bson import ObjectId

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dashing
collection = db.prefrences


def Check(usr_, pass_):
    check_var = db.users.find({'email': usr_})
    for val_ in check_var:
        if val_['email'] == usr_ and val_['password'] == pass_:
            return True
        else:
            return False

        
def Reddit(usr_r, text_r):
    val=db.prefrences.find({'email': usr_r})
    for v in val:
        var_ = v['reddit']
        if text_r in var_:
            return False
        else:
            collection.find_and_modify(query = {'email': usr_r}, update = {'$push':{ 'reddit': text_r}},upsert=True)
    
    
def Twitter(usr_t, text_t):
    val=db.prefrences.find({'email': usr_t})
    for v in val:
        var_ = v['twitter']
        if text_t in var_:
            return False
        else:
            collection.find_and_modify(query = {'email': usr_t}, update = {'$push':{ 'twitter': text_t}},upsert=True)
    
    
def Youtube(usr_y, text_y):
    val=db.prefrences.find({'email': usr_y})
    for v in val:
        var_ = v['youtube']
        if text_y in var_:
            return False
        else:
            collection.find_and_modify(query = {'email': usr_y}, update = {'$push':{ 'youtube': text_y}},upsert=True)
    
def News(usr_n, text_n):
    val=db.prefrences.find({'email': usr_n})
    for v in val:
        var_ = v['news']
        if text_n in var_:
            return False
        else:
            collection.find_and_modify(query = {'email': usr_n}, update = {'$push':{ 'news': text_n}},upsert=True)

    
def Api(usr_a):
    cursor = db.prefrences.find({'email': usr_a})   
    json_c = []
    for d in cursor:
        d['_id'] = str(d['_id'])
        dd = d
        json_c.append(dd)
    return json_c   
        
def RedditRemove(usr_rv,data_rv):

    val = collection.find_one({'email': usr_rv})
    red_var = val['reddit']
    for reddit in red_var:
        if reddit == data_rv:
            red_var.remove(reddit)
    collection.find_and_modify(query = {'email': usr_rv}, update = {'$set':{ 'reddit': red_var}},upsert=True)
    
def TwitterRemove(usr_tv,data_tv):

    val = collection.find_one({'email': usr_tv})
    tweet_var = val['twitter']
    for handles in tweet_var:
        if handles == data_tv:
            tweet_var.remove(handles)
    collection.find_and_modify(query = {'email': usr_tv}, update = {'$set':{ 'twitter': tweet_var}},upsert=True)
    
def YoutubeRemove(usr_yv,data_yv):

    val = collection.find_one({'email': usr_yv})
    you_var = val['youtube']
    for channel in you_var:
        if channel == data_yv:
            you_var.remove(channel)
    collection.find_and_modify(query = {'email': usr_yv}, update = {'$set':{ 'youtube': you_var}},upsert=True)
    
def NewsRemove(usr_nv,data_nv):

    val = collection.find_one({'email': usr_nv})
    news_var = val['news']
    for tags in news_var:
        if tags == data_nv:
            news_var.remove(tags)
    collection.find_and_modify(query = {'email': usr_nv}, update = {'$set':{ 'news': news_var}},upsert=True)
    
def Update():
    """os.chdir('sweet_dashboard_project')
    subprocess.call(["ls", "-l"])
    subprocess.call("dashing stop", shell=True)"""
    subprocess.call("bash /Users/Yu/dashing.sh", shell=True)
    
    
    
    
   

