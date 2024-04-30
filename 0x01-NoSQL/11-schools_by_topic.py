#!/usr/bin/env python3
""" MongoDB Operations with Python using pymongo """

def schools_by_topic(mongo_collection, topic):
    """Returns the list of schools having a specific topic"""
    # Find all schools that have the specified topic
    schools = mongo_collection.find({"topics": topic})
    return schools
