#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os
import tornado.web
import tornado.httpserver
import tornado.options
import tornado.locale

from mongoengine import connect
from settings import settings, WEB_ROOT_PATH
from base import BaseHandler
from course_demo import courseHandler
from tornado.options import define, options

connect(settings['db_name'], host=settings["db_host"], port=settings['db_port'])

class MainHandler(BaseHandler):
	def get(self):
		#print self.db.users.find()
		self.finish('tornado restful Server...!')
		return

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
			(r"/Course/[A-Za-z0-9]+", courseHandler), #GET
			(r"/Course/[A-Za-z0-9]+/[A-Za-z]+", courseHandler), #GET
			(r"/Course/?\.*", courseHandler), #GET
			(r"/Course/NEW", courseHandler), #POST
			(r"/Course/[A-Za-z0-9]+/UPDATE", courseHandler), #POST
			(r"/Course/[A-Za-z0-9]+/DELETE", courseHandler), #POST

        ]
        tornado.web.Application.__init__(self, handlers, **settings)

application = Application()

def main():
	tornado.options.parse_command_line()
	application.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	print "tornado restful server Started..."
	main()
