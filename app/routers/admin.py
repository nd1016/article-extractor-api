from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ArticleCache
from app.auth import create_access_token, get_current_admin

router = APIRouter(
    prefix="/admin",
    tags=["Admin Dashboard"]
)

# Hardcoded credentials for the single admin
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "supersecretpassword"

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Accepts a username and password, returns a JWT token if they match."""
    if form_data.username != ADMIN_USERNAME or form_data.password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Generate the token containing the username (the "sub" / subject)
    access_token = create_access_token(data={"sub": form_data.username})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/stats")
def get_api_stats(
    db: Session = Depends(get_db), 
    current_admin: str = Depends(get_current_admin)  # <-- This locks the route!
):
    """A protected route that returns database statistics."""
    # Count how many articles we have cached total
    total_cached = db.query(ArticleCache).count()
    
    return {
        "message": f"Welcome, {current_admin}!",
        "total_urls_cached": total_cached,
        "status": "Healthy"
    }