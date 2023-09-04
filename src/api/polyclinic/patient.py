from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from repositories.polyclinic import PatientRepository
from schemas.polyclinic import PatientRead, PatientCreate, PatientUpdate
from utils.depends import Pagination, UserFilter, patient_create, patient_update

router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
)


@router.get('', response_model=List[PatientRead])
async def get_list(pagination: Pagination = Depends(Pagination),
                   filters: UserFilter = Depends(UserFilter),
                   session: AsyncSession = Depends(get_session)):
    return await PatientRepository(session).get_user_filter_list(pagination.skip,
                                                                 pagination.limit,
                                                                 filters.phone,
                                                                 filters.email)


@router.get('/{patient_id}', response_model=PatientRead)
async def get_one(patient_id: int,
                  session: AsyncSession = Depends(get_session)):
    return await PatientRepository(session).get_one(patient_id)


@router.post('', response_model=PatientRead)
async def add_one(patient: PatientCreate = Depends(patient_create),
                  session: AsyncSession = Depends(get_session)):
    return await PatientRepository(session).add_one(patient)


@router.patch('/{patient_id}', response_model=PatientRead)
async def edit_one(patient_id: int,
                   patient: PatientUpdate = Depends(patient_update),
                   session: AsyncSession = Depends(get_session)):
    return await PatientRepository(session).edit_one(patient_id, patient)


@router.delete('/{patient_id}')
async def delete_one(patient_id: int,
                     session: AsyncSession = Depends(get_session)):
    return await PatientRepository(session).delete_one(patient_id)
