from fastapi import Query, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from models.polyclinic import Patient, Specialization, Qualification, Polyclinic, Doctor
from schemas.polyclinic import PatientCreate, PatientUpdate, DoctorCreate, DoctorUpdate, RouteCreate, RouteUpdate


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


async def doctor_create(doctor: DoctorCreate, session: AsyncSession = Depends(get_session)):
    specialization = await session.get(Specialization, doctor.specialization_id)
    if not specialization:
        raise HTTPException(status_code=404, detail="Specialization with this id not found")

    qualification = await session.get(Qualification, doctor.qualification_id)
    if not qualification:
        raise HTTPException(status_code=404, detail="Qualification with this id not found")

    polyclinic = await session.get(Polyclinic, doctor.polyclinic_id)
    if not polyclinic:
        raise HTTPException(status_code=404, detail="Polyclinic with this id not found")

    return doctor


async def doctor_update(doctor: DoctorUpdate, session: AsyncSession = Depends(get_session)):
    if doctor.specialization_id:
        specialization = await session.get(Specialization, doctor.specialization_id)
        if not specialization:
            raise HTTPException(status_code=404, detail="Specialization with this id not found")

    if doctor.qualification_id:
        qualification = await session.get(Qualification, doctor.qualification_id)
        if not qualification:
            raise HTTPException(status_code=404, detail="Qualification with this id not found")

    if doctor.polyclinic_id:
        polyclinic = await session.get(Polyclinic, doctor.polyclinic_id)
        if not polyclinic:
            raise HTTPException(status_code=404, detail="Polyclinic with this id not found")

    return doctor


async def route_create(route: RouteCreate, session: AsyncSession = Depends(get_session)):
    res = await session.get(Doctor, route.doctor_id)
    if not res:
        raise HTTPException(status_code=404, detail="Doctor with this id not found")
    return route
