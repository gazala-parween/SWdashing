import web
from vali import *

render = web.template.render('templates/')
urls = (
    '/', 'index', '/edit', 'edit'
)

userData = {'username_':"",'password_':""}
#print userData
class index:
    def GET(self):
        userData['username_']= ""
        userData['password_']= ""
        return render.login()

    def POST(self):
        login= web.input()
        #print login
        userData['username_']= login['username']
        userData['password_']= login['password']
        v=check(login['username'], login['password'])
        print v
        if v==True:
            return render.welcome()
        else:
            return render.login()
        
class edit:
    def GET(self):
        print userData
        return render.edit()
        
    def POST(self):
        var_= web.input()
        tt= var_['subreddit']
        yy= userData['username_']
        edit_(tt,yy)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
    
    
    
    
    
    
    
   