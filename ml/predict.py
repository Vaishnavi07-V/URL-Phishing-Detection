import os
import joblib
import pandas as pd

from .feature_extraction import extract_url_features


# Get the folder where predict.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Load the trained model
MODEL_PATH = os.path.join(
    BASE_DIR,
    "url_phishing_model.pkl"
)

model = joblib.load(MODEL_PATH)


# Load the feature names
FEATURE_PATH = os.path.join(
    BASE_DIR,
    "url_model_features.pkl"
)

feature_names = joblib.load(FEATURE_PATH)


def predict_url(url):

    # Extract features from the URL
    features = extract_url_features(url)

    # Convert features into a DataFrame
    input_data = pd.DataFrame([features])

    # Make sure features are in the same order
    # used during training
    input_data = input_data[feature_names]

    # Make prediction
    prediction = model.predict(input_data)[0]

    # Get prediction probabilities
    probabilities = model.predict_proba(input_data)[0]

    # Highest probability
    confidence = max(probabilities)

    # Dataset mapping:
    # 0 = Phishing
    # 1 = Legitimate
    if prediction == 1:
        result = "Legitimate"
    else:
        result = "Phishing"

    # IMPORTANT: return the result
    return {
        "prediction": int(prediction),
        "result": result,
        "confidence": round(float(confidence), 3)
    }


if __name__ == "__main__":

    test_url = "http://www.teramill.com"

    result = predict_url(test_url)

    print("URL:", test_url)
    print("Prediction:", result["prediction"])
    print("Result:", result["result"])
    print("Confidence:", result["confidence"])