import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.book import NewBook, Availability
from repository import book_repository
from models.book import Book


async def list_books(
    db: AsyncSession,
    status: Optional[Availability] = None,
    author: Optional[str] = None,
    sort_by: Optional[str] = None,
    cursor: Optional[str] = None,
    limit: int = 10,
) -> tuple[list[Book], Optional[str]]:
    return await book_repository.page_after(
        db,
        status=status.value if status is not None else None,
        author=author,
        sort_by=sort_by,
        cursor=cursor,
        limit=limit,
    )


async def one_book(db: AsyncSession, book_id: str) -> Optional[Book]:
    return await book_repository.find(db, book_id)


async def make_book(db: AsyncSession, book_data: NewBook) -> Book:
    book_dict = {
        "id": str(uuid.uuid4()),
        "title": book_data.title,
        "author": book_data.author,
        "description": book_data.description,
        "status": book_data.status.value,
        "year": book_data.year,
    }
    return await book_repository.insert(db, book_dict)


async def drop_book(db: AsyncSession, book_id: str) -> bool:
    return await book_repository.remove(db, book_id)
