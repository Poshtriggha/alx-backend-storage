#!/usr/bin/env python3
"""Python function that retrieves schools with a specific topic"""


def get_schools_by_topic(mongo_collection, topic):
    """Retrieve schools with a specific topic"""
    return list(mongo_collection.find({"topics": topic}))

