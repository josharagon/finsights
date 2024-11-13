from trading import handler as trading_handler
from sentiment import handler as sentiment_handler
import json

def handler(event, context):
    query = event.get('queryStringParameters', {})
    path = query.get('path', '')

    # Route requests based on 'path' query parameter
    if path == 'trading':
        return trading_handler(event, context)
    elif path == 'sentiment':
        return sentiment_handler(event, context)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid path'})
        }
