from typing import List, Dict, Optional
from models.book import _store


async def list_records() -> List[Dict]:
    return list(_store)


async def find(book_id: str) -> Optional[Dict]:
    for book in _store:
        if book["id"] == book_id:
            return book
    return None


async def insert(book_data: Dict) -> Dict:
    _store.append(book_data)
    return book_data


async def remove(book_id: str) -> bool:
    for i, book in enumerate(_store):
        if book["id"] == book_id:
            _store.pop(i)
            return True
    return False
