#!/usr/bin/env python3
""" MongoDB Operations with Python using pymongo """

def top_students(mongo_collection):
    """Returns all students sorted by average score"""
    # Get all students from the collection
    all_students = mongo_collection.find()

    # Calculate the average score for each student
    for student in all_students:
        total_score = sum(topic['score'] for topic in student['topics'])
        average_score = total_score / len(student['topics'])
        student['averageScore'] = round(average_score, 2)

    # Sort students by average score in descending order
    sorted_students = sorted(all_students, key=lambda x: x['averageScore'], reverse=True)

    return sorted_students

