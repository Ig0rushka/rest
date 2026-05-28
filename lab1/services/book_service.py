import uuid
from typing import List, Dict, Optional
from schemas.book import NewBook, Availability
from repository import book_repository


async def list_books(
    status: Optional[Availability] = None,
    author: Optional[str] = None,
    sort_by: Optional[str] = None,
) -> List[Dict]:
    books = await book_repository.list_records()

    if status is not None:
        books = [b for b in books if b["status"] == status.value]

    if author is not None:
        books = [b for b in books if author.lower() in b["author"].lower()]

    if sort_by == "title":
        books = sorted(books, key=lambda b: b["title"].lower())
    elif sort_by == "year":
        books = sorted(books, key=lambda b: b["year"])

    return books


async def one_book(book_id: str) -> Optional[Dict]:
    return await book_repository.find(book_id)


async def make_book(book_data: NewBook) -> Dict:
    book_dict = {
        "id": str(uuid.uuid4()),
        **book_data.model_dump(),
    }
    return await book_repository.insert(book_dict)


async def drop_book(book_id: str) -> bool:
    return await book_repository.remove(book_id)
