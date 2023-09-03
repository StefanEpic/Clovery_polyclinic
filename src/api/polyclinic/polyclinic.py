from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from repositories.polyclinic import PolyclinicRepository
from schemas.polyclinic import PolyclinicRead, PolyclinicCreate, PolyclinicUpdate
from utils.depends import Pagination

router = APIRouter(
    prefix="/polyclinics",
    tags=["Polyclinics"],
)


@router.get('', response_model=List[PolyclinicRead])
async def get_list(pagination: Pagination = Depends(Pagination),
                   session: AsyncSession = Depends(get_session)):
    return await PolyclinicRepository(session).get_list(pagination.skip, pagination.limit)


@router.get('/{polyclinic_id}', response_model=PolyclinicRead)
async def get_one(polyclinic_id: int,
                  session: AsyncSession = Depends(get_session)):
    return await PolyclinicRepository(session).get_one(polyclinic_id)


@router.post('', response_model=PolyclinicRead)
async def add_one(polyclinic: PolyclinicCreate,
                  session: AsyncSession = Depends(get_session)):
    return await PolyclinicRepository(session).add_one(polyclinic)


@router.patch('/{polyclinic_id}', response_model=PolyclinicRead)
async def edit_one(polyclinic_id: int,
                   polyclinic: PolyclinicUpdate,
                   session: AsyncSession = Depends(get_session)):
    return await PolyclinicRepository(session).edit_one(polyclinic_id, polyclinic)


@router.delete('/{polyclinic_id}')
async def delete_one(polyclinic_id: int,
                     session: AsyncSession = Depends(get_session)):
    return await PolyclinicRepository(session).delete_one(polyclinic_id)
