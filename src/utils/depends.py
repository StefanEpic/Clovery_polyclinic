from fastapi import Query, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from models.polyclinic import Patient
from schemas.polyclinic import PatientCreate, PatientUpdate


class Pagination:
    def __init__(self, skip: int = 0, limit: int = Query(default=100, lte=100)):
        self.skip = skip
        self.limit = limit


class UserFilter:
    def __init__(self, phone: str = None, email: str = None):
        self.phone = phone
        self.email = email


async def patient_create(patient: PatientCreate, session: AsyncSession = Depends(get_session)):
    res = await session.get(Patient, patient.polyclinic_id)
    if not res:
        raise HTTPException(status_code=404, detail="Polyclinic with this id not found")
    return patient


async def patient_update(patient: PatientUpdate, session: AsyncSession = Depends(get_session)):
    if patient.polyclinic_id:
        res = await session.get(Patient, patient.polyclinic_id)
        if not res:
            raise HTTPException(status_code=404, detail="Polyclinic with this id not found")
    return patient
