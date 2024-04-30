#!/usr/bin/env python3

"""
Script to list all databases in MongoDB.
"""

import pymongo

def list_databases():
    """List all databases in MongoDB."""
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    
    # List all databases
    databases = client.list_database_names()
    
    # Print the list of databases
    for db in databases:
        print(db)

if __name__ == "__main__":
    list_databases()

