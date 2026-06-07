from sqlalchemy.orm import Session

from app.models import Item
from app.schemas import ItemCreate, ItemUpdate


def create_item(db: Session, item: ItemCreate) -> Item:
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_item(db: Session, item_id: int) -> Item | None:
    return db.get(Item, item_id)


def get_items(db: Session, skip: int = 0, limit: int = 100) -> list[Item]:
    return db.query(Item).offset(skip).limit(limit).all()


def update_item(db: Session, item_id: int, item: ItemUpdate) -> Item | None:
    db_item = get_item(db, item_id=item_id)
    if db_item is None:
        return None

    update_data = item.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)

    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int) -> bool:
    db_item = get_item(db, item_id=item_id)
    if db_item is None:
        return False

    db.delete(db_item)
    db.commit()
    return True
