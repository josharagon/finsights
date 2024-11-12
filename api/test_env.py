# test_env.py

# Import the handler function from trading.py (no need for 'api.' prefix since it's in the same folder)
from trading import handler

# Simulate an API Gateway event with query parameters
event = {
    'queryStringParameters': {'endpoint': 'congress'}  # Change endpoint value to test other handlers
}

# Call the handler function
response = handler(event, None)

# Print the response to verify
print("Status Code:", response['statusCode'])
print("Response Body:", response['body'])
