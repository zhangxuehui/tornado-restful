#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       settings.py
#
import os
import tornado.web
import tornado.locale
from tornado.options import define, options

define("port", default=8888, help="tornado restful web Server", type=int)

###########################################################
#
#	Add current path into system path
#
###########################################################
WEB_ROOT_PATH = os.path.dirname(__file__)
import sys
sys.path.append(WEB_ROOT_PATH)


settings = dict(
    cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    #---mongodb settings---#
    db_host = '127.0.0.1',
    db_port = 27017,
    db_name = 'restDemo',
    max_pool_size = 100,
    #db_maxconnections = 10,
    root_url = WEB_ROOT_PATH,
    

)


