import hashlib
import Cookie
import base64
import web
import json
from vali import *
#from http import cookies

render = web.template.render('templates/')
urls = (
    '/','index','/edit','edit','/reddit/','reddit','/twitter/','twitter','/youtube/','youtube','/news/','news','/api/','api','/redditRemove/','redditRemove','/twitterRemove/','twitterRemove','/youtubeRemove/','youtubeRemove','/newsRemove/','newsRemove','/update/','update','/logout/','logout','/login','login','/createUser/','createUser'
)

app = web.application(urls, globals())
userData = {'username_':"",'password_':"",'user_id':""}
session = web.session.Session(app, web.session.DiskStore('sessions'))



class login:
    def GET(self):
        return render.login()

    def POST(self):
        login= web.input()
        userData['username_']= login['username']
        val=Check(login['username'], login['password'])
        if val==True:
            session.logged_in =True
            cookiestr= str(userData['username_'])
            cookie=base64.b64encode(cookiestr).decode('ascii')
            web.setcookie('test', cookie, 3600)
            #print "login post"
            userData['user_id']=Login(userData['username_'])
            raise web.seeother('/')
            
        else:
            return render.login()
        
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
            Reddit(usrr,textr)
        
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
            Twitter(usrt,textt)
        
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
            Youtube(usry,texty)
            
class news:
    def POST(self):
        cookieval=web.cookies().get('test')
        if cookieval:
            web.setcookie('test',cookieval,3600)
            web.header('Content-Type', 'application/json')
            web.header("Access-Control-Allow-Origin","*")
            data= web.input()
            usrn= userData['user_id']
            textn= data['newsText']
            News(usrn,textn)
        
class api:
    def GET(self):
#        cookieval=web.cookies().get('test')
#        if cookieval:
#            web.setcookie('test',cookieval,3600)
        usra= userData['user_id']
        _id = userData['user_id'] 
#            data = Api(_id)

        i= web.input()
        print i.user_id
        data = Api(i.user_id)
#            data = Api()
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
        
class update:
    def GET(self):
        cookieval=web.cookies().get('test')
        if cookieval:
            web.setcookie('test',cookieval,3600)
            data=web.input()
            Update()
        
          
if __name__ == "__main__":
    
    app.run()
    
    
    
    
    
    
    
   