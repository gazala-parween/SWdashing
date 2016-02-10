import os, os.path
from whoosh import index
#from whoosh.index import create_in
from whoosh.fields import Schema, TEXT

schema =Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
ix = index.create_in("redditWhoosh", schema)
writer = ix.writer()
writer.add_document(title=u"First document", path=u"/a",
                    content=u"This is the first document we've added!")
writer.add_document(title=u"Second document", path=u"/b",
                    content=u"The second one is even more interesting!")
writer.commit()

