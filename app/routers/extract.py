import hashlib
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Import your setup tools
from app.database import get_db  # Make sure this matches your database.py file
from app.models import ArticleCache
from app.utils.extractor import scrape_article

router = APIRouter(
    prefix="/extract",
    tags=["Extraction Engine"]
)

def generate_url_hash(url: str) -> str:
    """Converts a long URL into a uniform, fixed-length MD5 string for fast DB indexing."""
    return hashlib.md5(url.strip().lower().encode('utf-8')).hexdigest()

@router.post("/", status_code=status.HTTP_200_OK)
def extract_article(url: str, db: Session = Depends(get_db)):
    # Step 1: Generate unique hash of the URL
    url_hash = generate_url_hash(url)
    
    # Step 2: Query the database to see if we've already scraped this URL
    cached_article = db.query(ArticleCache).filter(ArticleCache.url_hash == url_hash).first()
    
    if cached_article:
        # Step 3: Check if the cache is older than 30 days
        # (Assuming created_at uses timezone-aware timestamps)
        age = datetime.now(timezone.utc) - cached_article.created_at
        if age < timedelta(days=30):
            print("🚀 Cache Hit! Serving directly from PostgreSQL database.")
            return {
                "source": "cache",
                "data": cached_article
            }
        else:
            print("⏳ Cache Expired! Re-scraping the URL.")
            # Optional: Delete the expired cache record so we don't duplicate rows
            db.delete(cached_article)
            db.commit()

    # Step 4: Cache Miss -> Run our working scraper service
    print("🌐 Cache Miss! Scraping live target...")
    scraped_data = scrape_article(url)
    
    if not scraped_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not extract data from the provided URL. Please verify the link is valid."
        )
        
    # Step 5: Save the newly scraped results back into PostgreSQL for future requests
    new_cache = ArticleCache(
        url_hash=url_hash,
        title=scraped_data.title,
        content=scraped_data.text,
        estimated_read_time=scraped_data.estimated_read_time,
        # Storing lists/extra elements in standard JSON fields
        keywords=scraped_data.keywords, 
        meta_data={
            "authors": scraped_data.authors,
            "top_image": scraped_data.top_image,
            "summary": scraped_data.summary
        }
    )
    
    db.add(new_cache)
    db.commit()
    db.refresh(new_cache)
    
    return {
        "source": "live_scraper",
        "data": new_cache
    }