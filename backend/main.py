from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from ml.predict import predict_url


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
        result = predict_url(str(request.url))

        return {
            "url": str(request.url),
            "prediction": result["prediction"],
            "result": result["result"],
            "confidence": result["confidence"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )