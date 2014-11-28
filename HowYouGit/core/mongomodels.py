from mongoengine import *

class Contributor(EmbeddedDocument):
	username = StringField(max_length=200, required=True)

class Follower(EmbeddedDocument):
	username = StringField(max_length=200, required=True)

class Repository(EmbeddedDocument):
	name = StringField(max_length=200, required=True)
	url = URLField(required=True)
	description = StringField(max_length=2500)
	commits = IntField(required=True)
	stargazers = IntField(required=True)
	forks = IntField(required=True)
	language = StringField(max_length=100, required=True)
	contributors = ListField(EmbeddedDocumentField(Contributor))

class User(Document):
	username = StringField(max_length=200, required=True)
	location = StringField(max_length=200, required=True)
	followers = ListField(EmbeddedDocumentField(Follower))
	repositories = ListField(EmbeddedDocumentField(Repository))