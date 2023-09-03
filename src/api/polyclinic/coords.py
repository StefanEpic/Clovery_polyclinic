from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from repositories.polyclinic import CoordsRepository
from schemas.polyclinic import CoordsRead, CoordsCreate, CoordsUpdate
from utils.depends import Pagination

router = APIRouter(
    prefix="/coords",
    tags=["Coords"],
)


@router.get('', response_model=List[CoordsRead])
async def get_list(pagination: Pagination = Depends(Pagination),
                   session: AsyncSession = Depends(get_session)):
    return await CoordsRepository(session).get_list(pagination.skip, pagination.limit)


@router.get('/{coords_id}', response_model=CoordsRead)
async def get_one(coords_id: int,
                  session: AsyncSession = Depends(get_session)):
    return await CoordsRepository(session).get_one(coords_id)


@router.post('', response_model=CoordsRead)
async def add_one(coords: CoordsCreate,
                  session: AsyncSession = Depends(get_session)):
    return await CoordsRepository(session).add_one(coords)


@router.patch('/{coords_id}', response_model=CoordsRead)
async def edit_one(coords_id: int,
                   coords: CoordsUpdate,
                   session: AsyncSession = Depends(get_session)):
    return await CoordsRepository(session).edit_one(coords_id, coords)


@router.delete('/{coords_id}')
async def delete_one(coords_id: int,
                     session: AsyncSession = Depends(get_session)):
    return await CoordsRepository(session).delete_one(coords_id)
