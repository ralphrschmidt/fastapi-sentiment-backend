import os
from typing import List
from fastapi import FastAPI
from .schemas import InputText
from .predictor import classifier
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


# 🔹 Detect the environment (default to "development" if not set)
ENV = os.getenv("ENV", "development")  # "development" or "production"
LOCALHOST_ORIGIN = os.getenv("LOCALHOST_ORIGIN", "http://localhost:8000")
REMOTEHOST_ORIGIN = os.getenv("REMOTEHOST_ORIGIN", "https://ralphrschmidt.github.io/fastapi-sentiment-frontend/")

# 🔹 Allow different CORS origins based on environment
#   If your website wants to fetch something from an api endpoint in a different
#   domain you have to state this explicitly, otherwise your browser will not 
#   allow you to do it (due to security concenrs)
if ENV == "development":
    allow_origins =  [LOCALHOST_ORIGIN] # Allow local testing
else:
    allow_origins = [REMOTEHOST_ORIGIN]  # Restrict in production

# ───────────────────────────────────────────────────────────────────────
# CORS Middleware Explanation
#
# This middleware enables Cross-Origin Resource Sharing (CORS), which allows 
# or restricts requests from different origins (domains). This is important 
# because, by default, browsers block cross-origin requests for security.
#
# - `allow_origins=allow_origins` → Specifies which domains can access the API
#   - In development, allows `http://localhost:8000`
#   - In production, allows `https://your-frontend.github.io`
# - `allow_credentials=True` → Allows sending cookies, auth headers, etc.
# - `allow_methods=["*"]` → Permits all HTTP methods (GET, POST, PUT, DELETE, etc.)
# - `allow_headers=["*"]` → Permits all request headers
#
# 🔹 Why Use This?
# - Ensures local testing works in development
# - Restricts frontend access in production for security
# - Prevents browsers from blocking API requests due to CORS policies
# ───────────────────────────────────────────────────────────────────────

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def home():
    return {"message": "FastAPI on AWS Lambda"}

@app.post("/predict/")
async def predict(data: InputText) -> List[dict]:
    """
    Accepts an InputText object and returns the model's prediction.
    """
    results = classifier(data.text)

    all_results = [
        {"label": result["label"], "score": result["score"]}
        for result in results  # Return all predictions in the list
    ]
    return all_results

# # For google cloud run which uses port 8080
# # Run Uvicorn with the port frosm the environment variable (Cloud Run uses PORT=8080)
# if __name__ == "__main__":
#     import uvicorn
#     port = int(os.environ.get("PORT", 8080))  # Cloud Run expects PORT=8080
#     uvicorn.run(app, host="0.0.0.0", port=port)