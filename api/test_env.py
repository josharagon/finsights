from index import handler

# Test sentiment endpoint
event = {
    'queryStringParameters': {
        'path': 'sentiment',
        'endpoint': 'wallstreetbets'
    }
}
response = handler(event, None)
print("Sentiment Response:", response)
