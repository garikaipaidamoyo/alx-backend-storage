#!/usr/bin/env python3

from pymongo import MongoClient


def get_log_stats(collection):
    # Get the total number of logs
    total_logs = collection.count_documents({})

    # Count the number of logs for each HTTP method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: collection.count_documents(
        {"method": method}) for method in methods}

    # Count the number of logs with method=GET and path=/status
    status_check_count = collection.count_documents(
            {"method": "GET", "path": "/status"}
    )

    return total_logs, method_counts, status_check_count


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    total_logs, method_counts, status_check_count = \
            your_function_that_gets_stats()   

    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"    method {method}: {count}")
    print(f"{status_check_count} status check")
