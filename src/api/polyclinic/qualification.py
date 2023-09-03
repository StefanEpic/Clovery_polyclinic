from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from repositories.polyclinic import QualificationRepository
from schemas.polyclinic import QualificationRead, QualificationCreate, QualificationUpdate
from utils.depends import Pagination

router = APIRouter(
    prefix="/qualifications",
    tags=["Qualifications"],
)


@router.get('', response_model=List[QualificationRead])
async def get_list(pagination: Pagination = Depends(Pagination),
                   session: AsyncSession = Depends(get_session)):
    return await QualificationRepository(session).get_list(pagination.skip, pagination.limit)


@router.get('/{qualification_id}', response_model=QualificationRead)
async def get_one(qualification_id: int,
                  session: AsyncSession = Depends(get_session)):
    return await QualificationRepository(session).get_one(qualification_id)


@router.post('', response_model=QualificationRead)
async def add_one(qualification: QualificationCreate,
                  session: AsyncSession = Depends(get_session)):
    return await QualificationRepository(session).add_one(qualification)


@router.patch('/{qualification_id}', response_model=QualificationRead)
async def edit_one(qualification_id: int,
                   qualification: QualificationUpdate,
                   session: AsyncSession = Depends(get_session)):
    return await QualificationRepository(session).edit_one(qualification_id, qualification)


@router.delete('/{qualification_id}')
async def delete_one(qualification_id: int,
                     session: AsyncSession = Depends(get_session)):
    return await QualificationRepository(session).delete_one(qualification_id)
