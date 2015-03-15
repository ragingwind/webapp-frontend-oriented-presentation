#!/usr/bin/env python

#  DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
# 
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
# 
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
# 
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
# 
#  0. You just DO WHAT THE FUCK YOU WANT TO.

import os
import logging
import cgi
import datetime
import urllib

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from django.utils import simplejson as json
from google.appengine.ext.webapp import template
from google.appengine.ext import db

# User data model
class User(db.Model):
 	name = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)
	
	@staticmethod
	def key(username):
		return db.Key.from_path('Users', username)

# handle it, http://web-applications-on-gae.appspot.com/		
class MainHandler(webapp.RequestHandler):
	def get(self):
		template_values = {}
		path = os.path.join(os.path.dirname(__file__), 'main.html')
		self.response.out.write(template.render(path, template_values))

# handle it, http://web-applications-on-gae.appspot.com/user
class UserHandler(webapp.RequestHandler):
	def post(self):
		username = cgi.escape(self.request.get('username'))
		user = User(parent=User.key(username))
		user.name = username
		user.put()

# handle it, http://web-applications-on-gae.appspot.com/users
class UsersListHandler(webapp.RequestHandler):
	def get(self):
		response = []	
		users = db.GqlQuery('SELECT * FROM User ORDER BY date DESC LIMIT 10')
		logging.debug(self)
		
		for user in users:
			userobj = {'name':user.name, 'date':str(user.date)}
			response.append(userobj)

		self.response.headers['Content-Type'] = "application/json"
		self.response.out.write(json.dumps(response))

# handle it, http://web-applications-on-gae.appspot.com/users/ragingwind
class UsersHandler(webapp.RequestHandler):
	def get(self, username):
		logging.debug(username)
		response = []	
		users = db.GqlQuery("SELECT * FROM User WHERE name = '" + username + "'")
		logging.debug(self)
		
		for user in users:
			userobj = {'name':user.name, 'date':str(user.date)}
			response.append(userobj)

		self.response.headers['Content-Type'] = "application/json"
		self.response.out.write(json.dumps(response))


def main():
	logging.getLogger().setLevel(logging.DEBUG)
	application = webapp.WSGIApplication([
		('/', MainHandler),
		(r"/user", UserHandler),
		(r"/users", UsersListHandler),
		(r"/users/([a-zA-Z0-9-]+)", UsersHandler)
	], debug=True)
	util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
