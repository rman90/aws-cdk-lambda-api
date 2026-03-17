import json


def handler(event, context):
    print("Event received:", json.dumps(event))

    path = event.get("path", "/")
    http_method = event.get("httpMethod", "GET")

    if path == "/hello" and http_method == "GET":
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Hello from AWS Lambda via API Gateway!"}),
        }

    if path == "/health" and http_method == "GET":
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"status": "healthy"}),
        }

    return {
        "statusCode": 404,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"error": f"Route {http_method} {path} not found"}),
    }
