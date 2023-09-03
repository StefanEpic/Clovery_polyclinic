from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from repositories.polyclinic import SpecializationRepository
from schemas.polyclinic import SpecializationRead, SpecializationCreate, SpecializationUpdate
from utils.depends import Pagination

router = APIRouter(
    prefix="/specializations",
    tags=["Specializations"],
)


@router.get('', response_model=List[SpecializationRead])
async def get_list(pagination: Pagination = Depends(Pagination),
                   session: AsyncSession = Depends(get_session)):
    return await SpecializationRepository(session).get_list(pagination.skip, pagination.limit)


@router.get('/{specialization_id}', response_model=SpecializationRead)
async def get_one(specialization_id: int,
                  session: AsyncSession = Depends(get_session)):
    return await SpecializationRepository(session).get_one(specialization_id)


@router.post('', response_model=SpecializationRead)
async def add_one(specialization: SpecializationCreate,
                  session: AsyncSession = Depends(get_session)):
    return await SpecializationRepository(session).add_one(specialization)


@router.patch('/{specialization_id}', response_model=SpecializationRead)
async def edit_one(specialization_id: int,
                   specialization: SpecializationUpdate,
                   session: AsyncSession = Depends(get_session)):
    return await SpecializationRepository(session).edit_one(specialization_id, specialization)


@router.delete('/{specialization_id}')
async def delete_one(specialization_id: int,
                     session: AsyncSession = Depends(get_session)):
    return await SpecializationRepository(session).delete_one(specialization_id)
