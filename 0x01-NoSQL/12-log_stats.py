#!/usr/bin/env python3
"""AAA"""

from pymongo import MongoClient

def get_nginx_logs_stats():
    client = MongoClient('mongodb://localhost:27017')
    db = client.logs
    nginx_collection = db.nginx

    total_logs = nginx_collection.count_documents({})
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: nginx_collection.count_documents({"method": method}) for method in methods}
    status_check_count = nginx_collection.count_documents({"method": "GET", "path": "/status"})

    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"    method {method}: {count}")
    print(f"{status_check_count} status check")

if __name__ == "__main__":
    get_nginx_logs_stats()

