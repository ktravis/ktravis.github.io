"""
models.py

App Engine datastore models

"""


from google.appengine.ext import ndb


class EntryModel(ndb.Model):
	title = ndb.StringProperty(required=True)
	text = ndb.TextProperty(required=True)
	slug = ndb.StringProperty(required=True)
	timestamp = ndb.DateTimeProperty(auto_now_add=True)
