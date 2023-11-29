from typing import List
from datetime import date, timedelta

from fastapi import Depends, HTTPException, status, Path, APIRouter
from sqlalchemy.orm import Session
from src.database.models import User, Role
from src.database.db import get_db
from src.repository import contacts as repository_contacts
from src.schemas import ContactResponse, ContactBase
from src.services.auth import auth_service
from src.services.roles import RoleAccess
router = APIRouter(prefix="/contacts", tags=["contacts"])

allowed_operation_get = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_create = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_update = RoleAccess([Role.admin, Role.moderator])
allowed_operation_remove = RoleAccess([Role.admin])


@router.get("/", response_model=List[ContactResponse], dependencies=[Depends(allowed_operation_get)], name="Return contacts")
async def get_contacts(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(db)
    return contacts


@router.get("/search_by_id/{id}", response_model=ContactResponse, dependencies=[Depends(allowed_operation_get)])
async def get_contact(id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_id(id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get(
    "/search_by_last_name/{last_name}",
    response_model=List[ContactResponse], dependencies=[Depends(allowed_operation_get)],
    name="Search contacts by last name",
)
async def search_contacts_by_last_name(last_name: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.search_contacts_by_last_name(last_name, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get(
    "/search_by_first_name/{first_name}",
    response_model=List[ContactResponse], dependencies=[Depends(allowed_operation_get)],
    name="Search contacts by first name",
)
async def search_contacts_by_first_name(first_name: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.search_contacts_by_first_name(first_name, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get(
    "/search_by_email/{email}",
    response_model=List[ContactResponse], dependencies=[Depends(allowed_operation_get)],
    name="Search contacts by email",
)
async def search_contacts_by_email(email: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.search_contact_by_email(email, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED,  dependencies=[Depends(allowed_operation_create)])
async def create_contacts(body: ContactBase, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_email(body.email, db)
    if contact:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email is exists!"
        )

    contact = await repository_contacts.create(body, db)
    return contact


@router.put("/{id}", response_model=ContactResponse,  dependencies=[Depends(allowed_operation_update)], description='Only moderators and admin')
async def update_contact(body: ContactBase, id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update(id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    return contact


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT,  dependencies=[Depends(allowed_operation_remove)], description='Only admin')
async def remove_contact(id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove(id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get(
    "/birthdays", response_model=List[ContactResponse], name="Upcoming Birthdays",  dependencies=[Depends(allowed_operation_get)]
)
async def get_birthdays(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    today = date.today()
    end_date = today + timedelta(days=7)
    birthdays = await repository_contacts.get_birthdays(today, end_date, db)
    if birthdays is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return birthdays
