from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from repositories.polyclinic import RouteRepository
from schemas.polyclinic import RouteRead, RouteCreate, RouteUpdate, RouteReadList
from utils.depends import Pagination, route_create

router = APIRouter(
    prefix="/routes",
    tags=["Routes"],
)


@router.get('', response_model=List[RouteReadList])
async def get_list(pagination: Pagination = Depends(Pagination),
                   session: AsyncSession = Depends(get_session)):
    return await RouteRepository(session).get_list(pagination.skip, pagination.limit)


@router.get('/{route_id}', response_model=RouteRead)
async def get_one(route_id: int,
                  session: AsyncSession = Depends(get_session)):
    return await RouteRepository(session).get_route(route_id)


@router.post('', response_model=RouteRead)
async def add_one(route: RouteCreate = Depends(route_create),
                  session: AsyncSession = Depends(get_session)):
    return await RouteRepository(session).add_route(route)


@router.patch('/{route_id}')
async def edit_one(route_id: int,
                   route: RouteUpdate,
                   session: AsyncSession = Depends(get_session)):
    return await RouteRepository(session).edit_route(route_id, route)


@router.delete('/{route_id}')
async def delete_one(route_id: int,
                     session: AsyncSession = Depends(get_session)):
    return await RouteRepository(session).delete_route(route_id)
