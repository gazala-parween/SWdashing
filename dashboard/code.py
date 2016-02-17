import hashlib
import Cookie
import base64
import web
import json
from vali import *


render = web.template.render('templates/')
urls = (
    '/','index','/edit','edit','/reddit/','reddit','/twitter/','twitter','/youtube/','youtube','/news/','news','/api/','api','/redditRemove/','redditRemove','/twitterRemove/','twitterRemove','/youtubeRemove/','youtubeRemove','/newsRemove/','newsRemove','/update/','update','/logout/','logout','/login','login','/createUser','createUser','/youtubeChannelId/','youtubeChannelId','/userApi/','userApi','/userRemove/','userRemove','/whooshSearch/','whooshSearch'
)

app = web.application(urls, globals())
userData = {'username_':"",'password_':"",'user_id':"",'perm':""}
session = web.session.Session(app, web.session.DiskStore('sessions'))

class login:
    def GET(self):
        return render.login("")

    def POST(self):
        login= web.input()
        userData['username_']= login['username']
        val=Check(login['username'], login['password'])
        if val==True:
            session.logged_in =True
            cookiestr= str(userData['username_'])
            cookie=base64.b64encode(cookiestr).decode('ascii')
            web.setcookie('test', cookie, 3600)
            valLog=Login(userData['username_'])
            userData['user_id']=str(valLog['_id'])
            userData['perm']=valLog['permission']
            print userData['user_id']
            print userData['perm']
            raise web.seeother('/')
        else:
            return render.login("INVALID CREDENTIALS!!")
        
class logout:
    def GET(self):
        web.setcookie('test', 'cookieunset', -100)
        raise web.seeother('/login')

class index:
    def GET(self):
        cookieval=web.cookies().get('test')
        if cookieval:
            web.setcookie('test',cookieval,3600)
            return render.index(userData)
        else:
            raise web.seeother('/login')
            
class edit:
    def GET(self):
        cookieval=web.cookies().get('test')
        if cookieval:
            web.setcookie('test',cookieval,3600)
            return render.edit()
        else:
            raise web.seeother('/login')
    
    def POST(self):
        return render.edit()
    
class createUser:
    def GET(self):
        return render.createUser()
    
    def POST(self):
        data=web.input()
        rval=CreateUser(data)
        o_id=str(rval['_id'])
        u_name=rval['username']
        CreateRecord(o_id,u_name)
        CreateRubyDashboard(o_id)
        CreateRubyJob(o_id)
        return render.createUser()

class reddit:
    def POST(self):
        cookieval=web.cookies().get('test')
        if cookieval:
            web.setcookie('test',cookieval,3600)
            web.header('Content-Type', 'application/json')
            web.header("Access-Control-Allow-Origin","*")
            data= web.input()
            usrr= userData['user_id']
            textr= data['redditText']
            chk=Reddit(usrr,textr)
            if chk:
                return json.dumps({"status":1})
            else:
                return json.dumps({"status":0})
            
            
        
class twitter:
    def POST(self):
        cookieval=web.cookies().get('test')
        if cookieval:
            web.setcookie('test',cookieval,3600)
            web.header('Content-Type', 'application/json')
            web.header("Access-Control-Allow-Origin","*")
            data= web.input()
            usrt= userData['user_id']
            textt= data['twitterText']
            chk=Twitter(usrt,textt)
            if chk:
                return json.dumps({"status":1})
            else:
                return json.dumps({"status":0})
        
class youtube:
    def POST(self):
        cookieval=web.cookies().get('test')
        if cookieval:
            web.setcookie('test',cookieval,3600)
            web.header('Content-Type', 'application/json')
            web.header("Access-Control-Allow-Origin","*")
            data= web.input()
            usry= userData['user_id']
            texty= data['youtubeText']
            chk=Youtube(usry,texty)
            if chk:
                return json.dumps({"status":1})
            else:
                return json.dumps({"status":0})
            
class news:
    def POST(self):
        cookieval=web.cookies().get('test')
        if cookieval:
            web.setcookie('test',cookieval,3600)
            web.header('Content-Type', 'application/json')
            web.header("Access-Control-Allow-Origin","*")
            data= web.input()
            print data
            usrn= userData['user_id']
            textn= data['newsText']
            chk=News(usrn,textn)
            if chk:
                return json.dumps({"status":1})
            else:
                return json.dumps({"status":0})
        
class api:
    def GET(self):
        usra= userData['user_id']
        _id = userData['user_id'] 
        i= web.input()
#         print i.user_id
        data = Api(i.user_id)
        web.header('Content-Type', 'application/json')
        web.header("Access-Control-Allow-Origin","*")
        return json.dumps(data)

class redditRemove:
    def POST(self):
        cookieval=web.cookies().get('test')
        if cookieval:
            web.setcookie('test',cookieval,3600)
            data= web.input()
            usrrv= userData['user_id']
            datar=data['redditRem']
            RedditRemove(usrrv,datar)
            
class twitterRemove:
    def POST(self):
        cookieval=web.cookies().get('test')
        if cookieval:
            web.setcookie('test',cookieval,3600)
            data= web.input()
            usrtv= userData['user_id']
            datat=data['twitterRem']
            TwitterRemove(usrtv,datat)
            
            
class youtubeRemove:
    def POST(self):
        cookieval=web.cookies().get('test')
        if cookieval:
            web.setcookie('test',cookieval,3600)
            data= web.input()
            usryv= userData['user_id']
            datay=data['youtubeRem']
            YoutubeRemove(usryv,datay)
            
            
class newsRemove:
    def POST(self):
        cookieval=web.cookies().get('test')
        if cookieval:
            web.setcookie('test',cookieval,3600)
            data= web.input()
            usrnv= userData['user_id']
            datan=data['newsRem']
            NewsRemove(usrnv,datan)
            
class youtubeChannelId:
    def GET(self):
        data= web.input()
        d=data['searchText']
        ch_id=Youtube_channelId_search(d)
        return ch_id
        
class update:
    def GET(self):
        cookieval=web.cookies().get('test')
        if cookieval:
            web.setcookie('test',cookieval,3600)
            data=web.input()
            Update()
            
class whooshSearch:
    def GET(self):
      		web.header('Content-Type', 'application/json')
       		web.header("Access-Control-Allow-Origin","*")
       		i= web.input()
       		pre_= WhooshSearch(i.user_id)
       		return json.dumps(pre_)
        
class userApi:
    def GET(self):
        db=UserApi()
        return db
    
class userRemove:
     def POST(self):
        cookieval=web.cookies().get('test')
        if cookieval:
            web.setcookie('test',cookieval,3600)
            data= web.input()
            usrName=data['userRem']
            UserRemove(usrName)


if __name__ == "__main__":
    
    app.run()
    



    
    
    
    
    
    
   