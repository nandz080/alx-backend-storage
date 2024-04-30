#!/usr/bin/env python3
""" MongoDB Operations with Python using pymongo """


def list_all(mongo_collection):
    """ List all documents in Python """
    listOfDocs = mongo_collection.find()

    # Use count_documents() to count the number of documents returned by the query
    if mongo_collection.count_documents({}) == 0:
        return []

    return listOfDocs

