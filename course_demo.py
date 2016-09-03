#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import BaseHandler, error_message, result_message

try:
    from bson.objectid import ObjectId
    from mongoengine import Document, StringField, IntField, SequenceField
except ImportError:
    raise ImportError


def convert_params(parms):
    '''Convert paramters whose type is not string
    '''
    for parm in parms:
        if parm.has_key('courseId'):
            parm['courseId'] = int(parm['courseId'])
        if parm.has_key('active'):
            parm['active'] = int(parm['active'])
    return parms


class Course(Document):
    '''Course class
    '''
    courseId = SequenceField()
    courseName = StringField(max_length=100)
    description = StringField(max_length=8000)
    suitableFor = StringField(max_length=200)
    courseLevel = StringField()
    language = StringField(max_length=100)
    active = IntField(default=1)  # 0 = inactive, 1 = active


class CourseHandler(BaseHandler):
    '''Course handler process GET | POST requests
        '''

    def get(self):
        try:
            rest = self.rest
            courses = []
            if rest['action'] == 'LIST':
                courses = Course.objects
            elif rest['action'] == 'FIND_ONE' or rest['action'] == 'QUERY':
                params = convert_params(rest['params'])
                if params:
                    q = {'$and': params}
                    courses = Course.objects(__raw__=(q))

            elif rest['action'] == 'FIND_RESOURCE':
                message = "Find %s of %s %s" % (
                    rest['resources'], rest['entity'], rest['params'])
                self.finish(message)

            if courses:
                self.finish(result_message(courses.to_json()))

        except Exception as error:
            self.finish(error_message(error.message))

    def post(self):
        try:
            courseName = self.get_argument('courseName', '')
            description = self.get_argument('description', '')
            suitableFor = self.get_argument('suitableFor', '')
            courseLevel = self.get_argument('courseLevel', '')
            language = self.get_argument('language', '')
            active = self.get_argument('active', 1)

            rest = self.rest
            # Create a new Course
            if rest['action'] == 'NEW':
                if Course.objects(courseName=courseName):
                    raise LookupError('Duplicate record')
                course = Course(courseName=courseName, description=description,
				                suitableFor=suitableFor, courseLevel=courseLevel,
								language=language, active=active)
                course.save()
                self.finish(result_message(course.to_json()))

            # Update or Delete a Course
            else:
                course_id = rest['params']
                course = Course.objects(id=ObjectId(course_id))[0]
                print course.to_json()
                if course:
                    # Delete a course : set the active = 0
                    if rest['action'] == 'DELETE':
                        Course.objects(id=ObjectId(course_id)).update_one(
                            active=0)  # or .remove()

                    # Update an existing course
                    if rest['action'] == 'UPDATE':
                        print 'update course'
                        Course.objects(id=ObjectId(course_id)).update_one(courseName=courseName,
                                                                          description=description,
                                                                          suitableFor=suitableFor,
                                                                          courseLevel=courseLevel,
                                                                          language=language,
                                                                          active=active)

                    self.finish(result_message(Course.objects(
                        id=ObjectId(course_id)).to_json()))
                else:
                    raise LookupError('Not found')

        except Exception as error:
            self.finish(error_message(error.message))
