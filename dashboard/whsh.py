import requests
import json
import os
import petl as etl
from whoosh.index import create_in
from whoosh.fields import *




r=requests.get("https://api.newswhip.com/v1/region/India/All/24?key=AHwaqz7hApx9D")
data = json.loads(r.text)

schema = Schema(title=TEXT(stored=True), publisher=TEXT(stored=True), excerpt=TEXT(stored=True), keywords=TEXT(stored=True), count=NUMERIC(stored=True))

dirname = 'dashing.whoosh'

if not os.path.exists(dirname):
    os.mkdir(dirname)
index = create_in('dashing.whoosh', schema)

writer = index.writer()

for i in data['articles']:
#    print i
    writer.add_document(title=unicode(i['headline'].encode('ascii', 'ignore')), excerpt=unicode(i['excerpt'].encode('ascii', 'ignore')), keywords=i['keywords'], publisher=i['source']['publisher'].rsplit('.',1)[0], count=i['fb_data']['like_count'] + i['tw_data']['tw_count'])

writer.commit()


