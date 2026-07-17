def test_extract_invalid_url(client):
    # Send a garbage URL to the API
    response = client.post("/extract/?url=not_a_real_website")
    
    # In our router, if scraping fails, we raise a 400 Bad Request
    assert response.status_code == 400
    assert "Could not extract data" in response.json()["detail"]

def test_extract_valid_url(client):
    # Send a known, working URL
    test_url = "https://en.wikipedia.org/wiki/FastAPI"
    response = client.post(f"/extract/?url={test_url}")
    
    # It should succeed and return the live_scraper source
    assert response.status_code == 200
    data = response.json()
    assert data["source"] == "live_scraper"
    assert "Wikipedia" in data["data"]["title"]  # Check if it actually grabbed the right title