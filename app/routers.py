"""Фабрика CRUD-роутерів.

Один і той самий набір ендпоінтів (GET-список, GET-один, POST, PUT, DELETE)
створюється для будь-якої сутності. Щоб додати новий ресурс, достатньо
викликати crud_router(...) у main.py — наявний код не змінюється (OCP).
"""

from collections.abc import Callable

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, SQLModel

from app.db import get_session
from app.repository import SQLModelRepository


def crud_router(
    *,
    prefix: str,
    tag: str,
    model: type[SQLModel],
    pk_name: str,
    create_schema: type[BaseModel],
    update_schema: type[BaseModel],
) -> APIRouter:
    """Будує роутер з повним набором CRUD-операцій для заданої сутності."""
    router = APIRouter(prefix=prefix, tags=[tag])

    def repo(session: Session = Depends(get_session)) -> SQLModelRepository:
        return SQLModelRepository(model, session, pk_name)

    @router.get("")
    def list_items(r: SQLModelRepository = Depends(repo)) -> list[model]:  # type: ignore[valid-type]
        return r.list()

    @router.get("/{item_id}")
    def get_item(item_id: str, r: SQLModelRepository = Depends(repo)) -> model:  # type: ignore[valid-type]
        obj = r.get(item_id)
        if obj is None:
            raise HTTPException(status_code=404, detail="Запис не знайдено")
        return obj

    @router.post("", status_code=201)
    def create_item(data: create_schema, r: SQLModelRepository = Depends(repo)) -> model:  # type: ignore[valid-type]
        return r.create(data.model_dump())  # type: ignore[attr-defined]

    @router.put("/{item_id}")
    def update_item(
        item_id: str,
        data: update_schema,  # type: ignore[valid-type]
        r: SQLModelRepository = Depends(repo),
    ) -> model:  # type: ignore[valid-type]
        obj = r.update(item_id, data.model_dump())  # type: ignore[attr-defined]
        if obj is None:
            raise HTTPException(status_code=404, detail="Запис не знайдено")
        return obj

    @router.delete("/{item_id}", status_code=204)
    def delete_item(item_id: str, r: SQLModelRepository = Depends(repo)) -> None:
        if not r.delete(item_id):
            raise HTTPException(status_code=404, detail="Запис не знайдено")

    # Callable нижче — лише щоб лінтер не вважав внутрішні функції невикористаними
    _handlers: tuple[Callable, ...] = (
        list_items,
        get_item,
        create_item,
        update_item,
        delete_item,
    )
    assert _handlers
    return router
