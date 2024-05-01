#!/usr/bin/env python3
"""Python function that returns specific topic"""


def schools_by_topic(mongo_collection, topic):
    """function that returns  specific topic"""
    return list(mongo_collection.find({"topics": topic}))
