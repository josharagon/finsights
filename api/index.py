from joblib import load
import pandas as pd
import json
from os.path import join, dirname
import os
from joblib import dump

# Add this debug code before loading the model
model_path = join(dirname(__file__), 'model.pkl')
print(f"Looking for model at: {model_path}")
print(f"File exists: {os.path.exists(model_path)}")

# Load pre-trained model
model = load(join(dirname(__file__), 'model.pkl'))

def handler(event, context):
    input_data = event.get('queryStringParameters', {})
    input_df = pd.DataFrame([input_data])
    
    prediction = model.predict(input_df)
    return {
        'statusCode': 200,
        'body': json.dumps({'prediction': prediction.tolist()})
    }
