#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Base handler module
'''
import tornado.web
import tornado.httpserver
import tornado.httpclient
import tornado.locale
import re, urlparse
try:
    from bson.objectid import ObjectId
except ImportError as error:
    print error.message
    raise ImportError

def error_message(message):
    '''returns error message in a dictionary
    '''
    return dict({'status':'ERROR', 'message':message})
def result_message(result):
    '''returns result message in a dictionary
    '''
    return dict({'status':'OK', 'data':result})
def parse_rest(uri):
    '''The function parses uri and returns the rest object
    '''
    rest = {}
    #/item/id/UPDATE    POST
    if re.match(r'/[A-Za-z]+/[A-Za-z0-9]+/(UPDATE|DELETE)', uri):
        uri_list = uri.split('/')
        rest['action'] = uri_list[3].split('?')[0]
        rest['params'] = uri_list[2]
        rest['entity'] = uri_list[1]
    #/item/id/resources GET
    elif re.match(r'/[A-Za-z]+/[A-Za-z0-9]+/[A-Za-z]+', uri):
        uri_list = uri.split('/')
        rest['action'] = 'FIND_RESOURCE'
        rest['resources'] = uri_list[3]
        rest['params'] = uri_list[2]
        rest['entity'] = uri_list[1]
    #/item/NEW          POST
    elif re.match(r'/[A-Za-z]+/NEW', uri):
        rest['action'] = 'NEW'
        rest['entity'] = uri.split('/')[1]
    #/item/LIST         GET
    elif re.match(r'/[A-Za-z]+/LIST', uri):
        rest['action'] = 'LIST'
        rest['entity'] = uri.split('/')[1]
        rest['params'] = []
    #/item/id           GET
    elif re.match(r'/[A-Za-z]+/[A-Za-z0-9]+', uri):
        uri_list = uri.split('/')
        rest['action'] = 'FIND_ONE'
        rest['entity'] = uri_list[1]
        rest['params'] = [{'_id': ObjectId(uri_list[2])}]
    #/item/?param1=v1&param2=v2&...     GET
    elif re.match(re.compile(r'/[A-Za-z]+/\?(.*)'), uri):
        query = urlparse.urlparse(uri).query
        rest['action'] = 'QUERY'
        rest['entity'] = uri.split('/')[1]
        rest['params'] = [{k:v[0]} for k, v in urlparse.parse_qs(query).items()]
    return rest

class BaseHandler(tornado.web.RequestHandler):
    '''This is the base handler class that can be overwrited
    in a other handler classes
    '''
    @property
    def rest(self):
        '''This function as a property returns the rest object
        '''
        return parse_rest(self.request.uri)

    def get(self):
        '''Action GET, this can be overwrited in concrete class
        '''
        try:
            #rest = parse_rest(self.request.uri)
            rest = self.rest
            #LIST
            if rest['action'] == 'LIST':
                pass
			#FIND_ONE | QUERY
            if rest['action'] == 'FIND_ONE' or rest['action'] == 'QUERY':
                params = rest['params']
                pass
            #FIND_RESOURCE
            if rest['action'] == 'FIND_RESOURCE':
                pass
        except Exception as error:
            self.finish(error_message(error.message))

    def post(self):
        '''Action POST, this can be overwrited in concrete class
        '''
        try:
            ###process request parameters###
            rest = self.rest
            # NEW
            if rest['action'] == 'NEW':
                pass
            # UPDATE | DELETE
            elif rest['action'] == 'DELETE':
                pass
            elif rest['action'] == 'UPDATE':
                pass
        except Exception as error:
            self.finish(error_message(error.message))
