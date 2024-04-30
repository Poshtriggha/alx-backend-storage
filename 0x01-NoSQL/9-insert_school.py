#!/usr/bin/env python3
"""Python function to add a new document to a collection"""


def add_document(mongo_collection, **kwargs):
    """Add a new document to a collection"""
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id

