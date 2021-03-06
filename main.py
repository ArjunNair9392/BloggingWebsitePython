#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import os 
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__),'template')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))


class Blog(db.Model):
	title = db.StringProperty(required = True)
	UserWriteUp = db.TextProperty(required =True)
	created = db.DateTimeProperty(auto_now_add = True)


class MainHandler(Handler):
    def render_front(self, title="", UserWriteUp="" ,error=""):
        UserWriteUp_table = db.GqlQuery("SELECT * FROM Blog "
    									"ORDER BY created DESC")

        self.render("blog.html", title=title, UserWriteUp=UserWriteUp, error=error, UserWriteUp_table=UserWriteUp_table)
    def get(self):
        self.render_front()

    def post(self):
  		UserWriteUp = self.request.get("UserWriteUp")
  		title = self.request.get("Title")

  		if UserWriteUp and title:
  			a = Blog(title = title, UserWriteUp = UserWriteUp)
			a.put()

			self.redirect("/")
  		else: 
  			error = "You have to write a blog and a title"
  	  		self.render_front(title, UserWriteUp ,error)

class CheckHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write("hey")

app = webapp2.WSGIApplication([
    ('/', MainHandler)
    ,
    ('/check',CheckHandler)
], debug=True)
