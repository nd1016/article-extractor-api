from datetime import datetime
from sqlalchemy import String, Text, Integer, JSON, DateTime, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Define the base class for declarative models
class Base(DeclarativeBase):
    pass

class ArticleCache(Base):
    __tablename__ = 'article_cache'

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Unique URL Hash (Indexed for faster lookups)
    url_hash: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    
    # Standard String/Text Columns
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    # JSON for flexible metadata (PostgreSQL natively supports this well)
    meta_data: Mapped[dict] = mapped_column(JSON, nullable=True)
    
    # PostgreSQL Array type for keywords
    keywords: Mapped[list[str]] = mapped_column(ARRAY(String).with_variant(JSON, "sqlite"), nullable=True)
    
    # Integer for read time (e.g., in minutes)
    estimated_read_time: Mapped[int] = mapped_column(Integer, nullable=True)
    
    # Timestamp, automatically set when the record is created
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )

    def __repr__(self) -> str:
        return f"<ArticleCache(id={self.id}, title='{self.title[:20]}...', url_hash='{self.url_hash}')>"