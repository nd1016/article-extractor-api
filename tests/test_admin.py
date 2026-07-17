def test_admin_stats_unauthorized(client):
    # Attempt to access the stats route without logging in
    response = client.get("/admin/stats")
    
    # It should block us with a 401 Unauthorized
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_admin_stats_authorized(client):
    # 1. First, log in to get the token
    login_response = client.post(
        "/admin/login", 
        data={"username": "admin", "password": "supersecretpassword"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # 2. Now use the token to access the protected route
    headers = {"Authorization": f"Bearer {token}"}
    stats_response = client.get("/admin/stats", headers=headers)
    
    # It should let us in!
    assert stats_response.status_code == 200
    assert stats_response.json()["status"] == "Healthy"