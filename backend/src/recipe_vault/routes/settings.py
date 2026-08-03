from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.orm import Session

from database import close_connection, create_connection

route = APIRouter(prefix="/settings", tags=["settings"])

@route.put("/update-email")
def update_email():
    pass

@route.put("/update-password")
def update_password():
    pass

@route.put("/update-username")
def update_username():
    pass

@route.delete("/delete-account")
def delete_account():
    pass