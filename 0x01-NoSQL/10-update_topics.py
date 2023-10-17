#!/usr/bin/env python3

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


def insert_school(collection, name, topics):
    try:
        result = collection.insert_one({
            "name": name,
            "topics": topics
        })
        return result.inserted_id
    except DuplicateKeyError:
        return None


def update_topics(collection, name, topics):
    return collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )


def main():
    client = MongoClient('mongodb://127.0.0.1:27017')
    school_collection = client.my_db.school

    # Insert schools with their initial topics
    insert_school(school_collection, "UCSF", [])
    insert_school(school_collection, "UCSD", [])
    insert_school(
        school_collection, "Holberton school",
        ['Sys admin', 'AI', 'Algorithm']
    )

    # Update topics for specific schools
    school_collection.update_one(
        {"name": "UCSF"},
        {"$set": {"topics": []}}
    )
    school_collection.update_one(
        {"name": "Holberton school"},
        {"$set": {"topics": ['iOS']}
    )

    # Print the schools
    for school in school_collection.find():
        print("[{}] {} {}".format(school['_id'], school['name'], school['topics']))


if __name__ == "__main__":
    main()
