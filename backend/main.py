from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator

from ml.predict import predict_url

from database.database import (
    initialize_database,
    insert_prediction,
    get_prediction_history
)


# Create FastAPI application
app = FastAPI(
    title="URL Phishing Detection API",
    description="API for detecting whether a URL is phishing or legitimate.",
    version="1.0.0"
)


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Initialize database when application starts
@app.on_event("startup")
def startup_event():
    initialize_database()


# Request model
class URLRequest(BaseModel):
    url: str

    @field_validator("url")
    @classmethod
    def validate_url(cls, value):

        value = value.strip()

        if not value.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")

        if len(value) <= 8:
            raise ValueError("Invalid URL")

        return value


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "URL Phishing Detection API is running"
    }


# Prediction endpoint
@app.post("/predict")
def predict(request: URLRequest):

    try:
        # Get prediction from existing ML model
        result = predict_url(str(request.url))

        prediction = result["prediction"]
        prediction_result = result["result"]
        confidence = result["confidence"]

        # Store prediction in SQLite database
        database_saved = insert_prediction(
            str(request.url),
            prediction,
            prediction_result,
            confidence
        )

        # Database failure should not prevent a successful ML response
        if not database_saved:
            print("Warning: Prediction was successful, but database storage failed.")

        return {
            "url": str(request.url),
            "prediction": prediction,
            "result": prediction_result,
            "confidence": confidence
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


# Prediction history endpoint
@app.get("/history")
def history():

    try:
        prediction_history = get_prediction_history()

        return {
            "history": prediction_history
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Could not retrieve prediction history: {str(e)}"
        )