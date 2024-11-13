from joblib import load
import pandas as pd
import json
from flask import Flask, request, jsonify
from os.path import join, dirname, abspath
import os

# Correct model path
model_path = abspath(join(dirname(__file__), '../models/trained_model.pkl'))
print(f"Looking for model at: {model_path}")
print(f"File exists: {os.path.exists(model_path)}")

# Load pre-trained model
if os.path.exists(model_path):
    model = load(model_path)
else:
    raise FileNotFoundError(f"Model not found at {model_path}. Ensure the model is saved correctly.")

# Initialize Flask app
app = Flask(__name__)

@app.route('/predict', methods=['GET'])
def predict():
    input_data = request.args.to_dict()  # Get query parameters as a dictionary
    input_df = pd.DataFrame([input_data])  # Convert to DataFrame

    try:
        # Ensure all inputs match the model's expected data types
        prediction = model.predict(input_df)
        response = {'prediction': prediction.tolist()}
    except ValueError as e:
        response = {'error': 'Data input error: ' + str(e)}
    except Exception as e:
        response = {'error': 'Prediction error: ' + str(e)}
    
    return jsonify(response)

if __name__ == '__main__':
    # Use debug mode for local testing only
    app.run(debug=True, host='0.0.0.0', port=5001)
