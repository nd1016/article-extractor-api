from fastapi import FastAPI
from app.routers import extract
from app.routers import extract, admin

# Initialize the FastAPI app
app = FastAPI(
    title="Universal Article & SEO Extractor API",
    description="An API that scrapes articles, extracts SEO metadata, and caches results.",
    version="1.0.0"
)

# Root Endpoint (Just a quick health check)
@app.get("/")
def root():
    return {"message": "Welcome to the Universal Article & SEO Extractor API. Head to /docs to test endpoints."}

# Include the routers for extraction and admin functionalities
app.include_router(extract.router)
app.include_router(admin.router)