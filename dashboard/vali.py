import pymongo

from pymongo import MongoClient


client = MongoClient('localhost',27017)
db = client.dashing


def check(usr,pass_):
    check_var = db.users.find({"email":usr})
    for v1 in check_var:
        print v1['email'],usr,v1['password'],pass_
        if (v1['email']==usr and v1['password']==pass_):
    #if (check_var['email']==usr and check_var['password']==pass_):
            return True
        else:
            return False
        
def edit_(var_,var2_):
#    print "enter"
#    db = client.test.prefrences
    
    
    reddit = {'subreddit_url':var_,'email':var2_}
    db.prefrences.insert(reddit)
    #print reddit
    return reddit
   # db.prefrences.find()
    #db.users.find()
    
    
    """
    
    
pseudo code for edit_

var= db.prefrences.find_one({"emailid": ""})
if reddit
var["subreddit_url"] =
"""
   
