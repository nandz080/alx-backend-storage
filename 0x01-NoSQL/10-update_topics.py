#!/usr/bin/env python3
""" MongoDB Operations with Python using pymongo """

def update_topics(mongo_collection, name, topics):
    """Updates topics of a school document based on the name"""
    # Update the topics of the school document with the provided name
    mongo_collection.update_one({"name": name}, {"$set": {"topics": topics}})
