#!/usr/bin/env python3
"""Script to provide stats about Nginx logs stored in MongoDB"""

from pymongo import MongoClient

def log_stats():
    """Function to provide stats about Nginx logs stored in MongoDB"""
    # Connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')

    # Access the logs database and nginx collection
    database = client.logs
    collection = database.nginx

    # Count the total number of logs
    total_logs = collection.count_documents({})

    print("{} logs".format(total_logs))

    # Count the number of logs for each method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        method_count = collection.count_documents({"method": method})
        print("    method {}: {}".format(method, method_count))

    # Count the number of logs with method=GET and path=/status
    status_count = collection.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(status_count))

if __name__ == "__main__":
    log_stats()

