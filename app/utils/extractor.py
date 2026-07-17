import nltk
from newspaper import Article, ArticleException
from pydantic import BaseModel
from typing import Optional, List
import math

# --- NEW IMPORT ---
from curl_cffi import requests

# Download necessary NLP corpora
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class ArticleData(BaseModel):
    title: str
    authors: List[str]
    publish_date: Optional[str]
    top_image: Optional[str]
    text: str
    keywords: List[str]
    summary: str
    estimated_read_time: int

def calculate_read_time(text: str, wpm: int = 200) -> int:
    word_count = len(text.split())
    read_time = math.ceil(word_count / wpm)
    return read_time

def scrape_article(url: str) -> Optional[ArticleData]:
    try:
        # 1. Download the HTML using curl_cffi to bypass Cloudflare
        # impersonate="chrome" perfectly fakes the browser's TLS encryption
        print(f"Bypassing Cloudflare to fetch: {url}...")
        response = requests.get(url, impersonate="chrome", timeout=15)
        
        # If the page doesn't exist, stop here
        if response.status_code != 200:
            print(f"Failed to fetch page. Status code: {response.status_code}")
            return None
            
        raw_html = response.text

        # 2. Initialize the Newspaper Article object
        article = Article(url)
        
        # 3. Manually inject the HTML and fake the download state
        article.html = raw_html
        article.download_state = 2  # 2 is newspaper's internal code for "SUCCESS"
        
        # 4. Parse and NLP as usual
        article.parse()
        article.nlp()
        
        read_time = calculate_read_time(article.text)
        
        return ArticleData(
            title=article.title,
            authors=article.authors,
            publish_date=str(article.publish_date) if article.publish_date else None,
            top_image=article.top_image,
            text=article.text,
            keywords=article.keywords,
            summary=article.summary,
            estimated_read_time=read_time
        )
        
    except ArticleException as e:
        print(f"Newspaper parsing failed. Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# --- Quick Test Block ---
if __name__ == "__main__":
    # A live article about AI
    test_url = "https://techcrunch.com/category/startups/"
    result = scrape_article(test_url)
    
    if result:
        print(f"\n✅ SUCCESS!")
        print(f"Title: {result.title}")
        print(f"Read Time: {result.estimated_read_time} minutes")
        print(f"Keywords: {result.keywords}")
        print(f"Preview: {result.text[:150]}...\n")
    else:
        print("\n❌ Failed to extract data.")