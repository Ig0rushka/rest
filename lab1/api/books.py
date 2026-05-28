from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from schemas.book import NewBook, BookRecord, Availability
from services import book_service

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=List[BookRecord], status_code=200)
async def get_books(
    status: Optional[Availability] = Query(None, description="Filter by book status"),
    author: Optional[str] = Query(None, description="Filter by author name (partial, case-insensitive)"),
    sort_by: Optional[str] = Query(None, pattern="^(title|year)$", description="Sort by: title or year"),
):
    return await book_service.list_books(status=status, author=author, sort_by=sort_by)


@router.get("/{book_id}", response_model=BookRecord, status_code=200)
async def get_book(book_id: str):
    book = await book_service.one_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/", response_model=BookRecord, status_code=201)
async def create_book(book: NewBook):
    return await book_service.make_book(book)


@router.delete("/{book_id}", status_code=204)
async def delete_book(book_id: str):
    deleted = await book_service.drop_book(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Not found")
