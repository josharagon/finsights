from quiver import quiver
import json

def handler(event, context):
    client = quiver()

    # Get query parameters
    query = event.get('queryStringParameters', {})
    endpoint = query.get('endpoint', 'wallstreetbets')  # Default to WallStreetBets

    if endpoint == 'wallstreetbets':
        df = client.wallstreetbets()
    elif endpoint == 'twitter':
        df = client.twitter()
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid endpoint'})
        }

    return {
        'statusCode': 200,
        'body': df.to_json(orient='records')
    }
