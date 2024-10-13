from fastapi import APIRouter
from .schemas import Item

router = APIRouter()


@router.get("/")
async def read_root():
    return {"message": "Welcome to the API"}


@router.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    return Item(id=item_id, name=f"Item {item_id}", description="A test item")
