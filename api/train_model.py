import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import pickle
import os
from data_pipeline import fetch_data
from dotenv import load_dotenv
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import GradientBoostingRegressor
import numpy as np

load_dotenv()  # Load .env variables

def train_model():
    # Fetch the data
    print("Fetching data...")
    data = fetch_data()
    
    # Ensure 'Amount' column is numeric
    data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')

    # Drop any rows with NaN 'Amount' values resulting from conversion
    data = data.dropna(subset=['Amount'])
    
    # Remove outliers from 'Amount'
    Q1 = data['Amount'].quantile(0.25)
    Q3 = data['Amount'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    data = data[(data['Amount'] >= lower_bound) & (data['Amount'] <= upper_bound)]
    
    # Feature engineering: Selecting features and target
    print("Preparing data for training...")
    
    # Define target and features
    target = np.log1p(data['Amount'])
    features = data.drop(columns=['Amount'])
    
    # Identify datetime columns and convert to numerical features
    datetime_cols = features.select_dtypes(include=['datetime64[ns]', 'datetime64']).columns.tolist()
    for col in datetime_cols:
        features[col] = features[col].apply(lambda x: x.timestamp())
    
    # Identify numerical columns
    numerical_cols = features.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    # Identify categorical columns (all object-type columns)
    categorical_cols = features.select_dtypes(include=['object']).columns.tolist()
    
    # Proceed with handling missing values
    features[categorical_cols] = features[categorical_cols].fillna('Unknown')
    features[numerical_cols] = features[numerical_cols].fillna(0)
    
    # Encode categorical variables
    features = pd.get_dummies(features, columns=categorical_cols, drop_first=True)
    
    # Ensure all features are numeric
    print("Verifying that all features are numeric...")
    if not all(features.dtypes != 'object'):
        print("Non-numeric columns found:")
        print(features.dtypes[features.dtypes == 'object'])
        raise ValueError("There are still non-numeric columns in features after encoding.")
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    
    # Define the parameter grid
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': ['auto', 'sqrt'],
    }

    # Initialize the model
    rf = RandomForestRegressor(random_state=42)

    # Initialize GridSearchCV
    grid_search = GridSearchCV(
        estimator=rf,
        param_grid=param_grid,
        cv=5,
        n_jobs=-1,
        scoring='neg_mean_squared_error',
        verbose=2
    )

    # Perform cross-validation
    cv_scores = cross_val_score(rf, features, target, cv=5, scoring='neg_mean_squared_error')
    mse_scores = -cv_scores
    mean_mse = mse_scores.mean()
    print(f"Cross-Validated Mean Squared Error: {mean_mse}")

    # Proceed to train on the full training set
    print("Training model with hyperparameter tuning...")
    grid_search.fit(X_train, y_train)

    # Best model
    best_model = grid_search.best_estimator_
    print(f"Best Parameters: {grid_search.best_params_}")

    # Evaluate the model
    print("Evaluating model...")
    predictions = best_model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"Optimized Model Mean Squared Error: {mse}")
    
    # Save the model
    print("Saving the trained model...")
    model_path = 'models/trained_model.pkl'
    os.makedirs('models', exist_ok=True)
    with open(model_path, 'wb') as f:
        pickle.dump(best_model, f)
    
    print("Training complete.")

    # Get feature importances
    feature_importances = pd.Series(best_model.feature_importances_, index=features.columns)
    important_features = feature_importances.nlargest(20)  # Top 20 features
    print("Top 20 Important Features:")
    print(important_features)

    # Optionally, retrain model using only important features
    important_feature_names = important_features.index.tolist()
    X_train_imp = X_train[important_feature_names]
    X_test_imp = X_test[important_feature_names]

    # Retrain the model on important features
    print("Retraining model with important features...")
    best_model.fit(X_train_imp, y_train)

    # Evaluate the model
    predictions = best_model.predict(X_test_imp)
    mse = mean_squared_error(y_test, predictions)
    print(f"Model Mean Squared Error with Important Features: {mse}")

    # Initialize the model
    model = GradientBoostingRegressor(n_estimators=100, random_state=42)

    # Train the model
    print("Training Gradient Boosting Regressor...")
    model.fit(X_train, y_train)

    # Evaluate the model
    print("Evaluating model...")
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"Gradient Boosting Model Mean Squared Error: {mse}")

    # Transform predictions back to original scale
    predictions_exp = np.expm1(predictions)
    y_test_exp = np.expm1(y_test)

    mse_original_scale = mean_squared_error(y_test_exp, predictions_exp)
    print(f"Model Mean Squared Error on Original Scale: {mse_original_scale}")

if __name__ == "__main__":
    token = os.getenv("QUIVER_API_TOKEN")
    if not token:
        raise ValueError("QUIVER_API_TOKEN is not set in your environment variables.")
    train_model()
