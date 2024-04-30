#!/usr/bin/env python3
""" MongoDB Operations with Python using pymongo """


def insert_school(mongo_collection, **kwargs):
    """ Inserts a new document in a collection based on kwargs """
    newdoc_id = mongo_collection.insert_one(kwargs).inserted_id
    return newdoc_id
