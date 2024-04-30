#!/usr/bin/env python3
""" MongoDB Operations with Python using pymongo """

def top_students(mongo_collection):
    """Returns all students sorted by average score"""
    students = mongo_collection.find()
    top_students = []

    for student in students:
        scores = [topic['score'] for topic in student['topics']]
        average_score = sum(scores) / len(scores) if scores else 0
        student['averageScore'] = average_score
        top_students.append(student)

    sorted_top_students = sorted(top_students, key=lambda x: x['averageScore'], reverse=True)
    return sorted_top_students
