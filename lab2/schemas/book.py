from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class Availability(str, Enum):
    AVAILABLE = "available"
    ISSUED = "issued"


class NewBook(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    status: Availability = Availability.AVAILABLE
    year: int = Field(..., ge=1000, le=2100)


class BookRecord(BaseModel):
    id: str
    title: str
    author: str
    description: Optional[str] = None
    status: Availability
    year: int

    model_config = {"from_attributes": True}


class PagedBooks(BaseModel):
    items: List[BookRecord]
    total: int
    limit: int
    offset: int
