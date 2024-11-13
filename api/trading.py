from quiver import quiver
import json

def handler(event, context):
    client = quiver()

    # Get query parameters
    query = event.get('queryStringParameters', {})
    endpoint = query.get('endpoint', 'congress')  # Default to congress trading

    # Route based on query parameter
    if endpoint == 'congress':
        df = client.congress_trading()
    elif endpoint == 'senate':
        df = client.senate_trading()
    elif endpoint == 'house':
        df = client.house_trading()
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid endpoint'})
        }

    # Return JSON data
    return {
        'statusCode': 200,
        'body': df.to_json(orient='records')
    }
