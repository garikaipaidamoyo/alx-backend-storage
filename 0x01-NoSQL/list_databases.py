# list_databases.py
from pymongo import MongoClient


def list_databases():
    client = MongoClient('mongodb://127.0.0.1:27017')
    databases = client.list_database_names()
    for db in databases:
        print(db)


if __name__ == "__main__":
    list_databases()
