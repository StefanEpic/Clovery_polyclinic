from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from repositories.polyclinic import DoctorRepository
from schemas.polyclinic import DoctorRead, DoctorCreate, DoctorUpdate, RouteRead
from utils.depends import Pagination

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"],
)


@router.get('', response_model=List[DoctorRead])
async def get_list(pagination: Pagination = Depends(Pagination),
                   session: AsyncSession = Depends(get_session)):
    return await DoctorRepository(session).get_list(pagination.skip, pagination.limit)


@router.get('/{doctor_id}', response_model=DoctorRead)
async def get_one(doctor_id: int,
                  session: AsyncSession = Depends(get_session)):
    return await DoctorRepository(session).get_one(doctor_id)


@router.get('/{doctor_id}/route', response_model=RouteRead)
async def get_one(doctor_id: int,
                  session: AsyncSession = Depends(get_session)):
    return await DoctorRepository(session).get_doctor_route(doctor_id)


@router.post('', response_model=DoctorRead)
async def add_one(doctor: DoctorCreate,
                  session: AsyncSession = Depends(get_session)):
    return await DoctorRepository(session).add_one(doctor)


@router.patch('/{doctor_id}', response_model=DoctorRead)
async def edit_one(doctor_id: int,
                   doctor: DoctorUpdate,
                   session: AsyncSession = Depends(get_session)):
    return await DoctorRepository(session).edit_one(doctor_id, doctor)


@router.delete('/{doctor_id}')
async def delete_one(doctor_id: int,
                     session: AsyncSession = Depends(get_session)):
    return await DoctorRepository(session).delete_one(doctor_id)
