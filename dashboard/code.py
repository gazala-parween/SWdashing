import hashlib
import Cookie
import base64
import web
import json
from vali import *
#from http import cookies

render = web.template.render('templates/')
urls = (
    '/','index','/edit','edit','/reddit/','reddit','/twitter/','twitter','/youtube/','youtube','/news/','news','/api/','api','/redditRemove/','redditRemove','/twitterRemove/','twitterRemove','/youtubeRemove/','youtubeRemove','/newsRemove/','newsRemove','/update/','update','/logout/','logout','/login','login',
)

app = web.application(urls, globals())
userData = {'username_':"",'password_':""}
session = web.session.Session(app, web.session.DiskStore('sessions'))

class index:
    def GET(self):
        cookieval=web.cookies().get('test')
        if cookieval:
            web.setcookie('test',cookieval,3600)
            return render.index(userData['username_'])
        else:
            raise web.seeother('/login')

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
            print "login post"
            raise web.seeother('/')
        else:
            return render.login()
        
class logout:
    def GET(self):
        web.setcookie('test', 'cookieunset', -100)
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

class reddit:
    def POST(self):
        cookieval=web.cookies().get('test')
        if cookieval:
            web.setcookie('test',cookieval,3600)
            web.header('Content-Type', 'application/json')
            web.header("Access-Control-Allow-Origin","*")
            data= web.input()
            usrr= userData['username_']
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
            usrt= userData['username_']
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
            usry= userData['username_']
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
            usrn= userData['username_']
            textn= data['newsText']
            News(usrn,textn)
        
class api:
    def GET(self):
#        cookieval=web.cookies().get('test')
#        if cookieval:
#            web.setcookie('test',cookieval,3600)
        usra= userData['username_']
        w_data = web.input()
        data = Api(usra)
        web.header('Content-Type', 'application/json')
        web.header("Access-Control-Allow-Origin","*")
        return json.dumps(data)

class redditRemove:
    def POST(self):
        cookieval=web.cookies().get('test')
        if cookieval:
            web.setcookie('test',cookieval,3600)
            data= web.input()
            usrrv= userData['username_']
            datar=data['redditRem']
            RedditRemove(usrrv,datar)
            
class twitterRemove:
    def POST(self):
        cookieval=web.cookies().get('test')
        if cookieval:
            web.setcookie('test',cookieval,3600)
            data= web.input()
            usrtv= userData['username_']
            datat=data['twitterRem']
            TwitterRemove(usrtv,datat)
            
            
class youtubeRemove:
    def POST(self):
        cookieval=web.cookies().get('test')
        if cookieval:
            web.setcookie('test',cookieval,3600)
            data= web.input()
            usryv= userData['username_']
            datay=data['youtubeRem']
            YoutubeRemove(usryv,datay)
            
            
class newsRemove:
    def POST(self):
        cookieval=web.cookies().get('test')
        if cookieval:
            web.setcookie('test',cookieval,3600)
            data= web.input()
            usrnv= userData['username_']
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
    
    
    
    
    
    
    
   