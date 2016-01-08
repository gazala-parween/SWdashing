import pprint
import csv
import json
import datetime

from NewsWhipAPILib.Controllers.NewsController import *

controller = NewsController()
"""
response = controller.get_region(key='AHwaqz7hApx9D')
#print response["articles"][0]["fb_data"]["like_count"]
articles = response["articles"]
for article in articles:
	print article["fb_data"]["comment_count"] , "," , article["fb_data"]["like_count"]
	#print article["fb_data"]["like_count"]
#print json.dumps(response)

#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(response)

"""



response = controller.get_region(key='AHwaqz7hApx9D') 
artriclesArr = response["articles"]
with open('news2.csv', 'w') as csvfile:
	writer=csv.writer(csvfile, delimiter=',',lineterminator='\n',)
    #data = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
   
    #data.writerow(['headline', 'comment_count', 'share_count', 'tw_count'])
	writer.writerow([datetime.datetime.now()])
	for article in artriclesArr:
		headlineStr = article["headline"]
		headlineStr.encode("utf-8")
		#headline = unicode(headlineStr, "utf-8")
		writer.writerow([  article["headline"].encode("utf-8"), article["fb_data"]["comment_count"], article["fb_data"]["like_count"] ])


