import requests
import json

# Define the endpoint
url = "http://127.0.0.1:5004/generate-report"

# Mock data to test
test_data = {
    "current_savings": 1000,
    "cash_flows": [
        {"amount": 2000, "flow_type": "Income", "frequency": "Monthly"},
        {"amount": 150, "flow_type": "Expense", "frequency": "Monthly"},
        {"amount": 500, "flow_type": "Income", "frequency": "One Time"},
        {"amount": 1200, "flow_type": "Expense", "frequency": "Annually"}
    ]
}

# Send request to microservice
response = requests.post(url, json=test_data)

# Print response
print("Response Code:", response.status_code)
print("Response JSON:", json.dumps(response.json(), indent=4))
