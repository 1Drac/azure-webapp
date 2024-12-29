from fastapi import APIRouter, Query, HTTPException
from sqlmodel import select
from typing import Annotated

from ..database import SessionDep