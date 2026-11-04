"""Абстракція сховища даних (принцип відкритості/закритості, OCP).

Роутери працюють з інтерфейсом Repository, а не з конкретною БД. Щоб додати
нове сховище (наприклад, MongoDB чи Redis), достатньо написати новий клас, що
реалізує цей інтерфейс, — наявний код змінювати не потрібно.
"""

from abc import ABC, abstractmethod

from sqlmodel import Session, SQLModel, select


class Repository[T: SQLModel](ABC):
    """Інтерфейс сховища для однієї сутності (CRUD-операції)."""

    @abstractmethod
    def list(self) -> list[T]: ...

    @abstractmethod
    def get(self, item_id: object) -> T | None: ...

    @abstractmethod
    def create(self, data: dict) -> T: ...

    @abstractmethod
    def update(self, item_id: object, data: dict) -> T | None: ...

    @abstractmethod
    def delete(self, item_id: object) -> bool: ...


class SQLModelRepository[T: SQLModel](Repository[T]):
    """Реалізація сховища на базі SQLModel/PostgreSQL для будь-якої моделі."""

    def __init__(self, model: type[T], session: Session, pk_name: str):
        self.model = model
        self.session = session
        self.pk_name = pk_name

    def list(self) -> list[T]:
        return list(self.session.exec(select(self.model)).all())

    def get(self, item_id: object) -> T | None:
        return self.session.get(self.model, item_id)

    def create(self, data: dict) -> T:
        obj = self.model(**data)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def update(self, item_id: object, data: dict) -> T | None:
        obj = self.session.get(self.model, item_id)
        if obj is None:
            return None
        for key, value in data.items():
            setattr(obj, key, value)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, item_id: object) -> bool:
        obj = self.session.get(self.model, item_id)
        if obj is None:
            return False
        self.session.delete(obj)
        self.session.commit()
        return True
