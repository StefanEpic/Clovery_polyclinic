import datetime
from typing import Optional

from pydantic import BaseModel


class SpecializationCreate(BaseModel):
    title: str
    description: str = None


class SpecializationRead(BaseModel):
    id: int
    title: str
    description: Optional[str]


class SpecializationUpdate(BaseModel):
    title: str = None
    description: str = None


class QualificationCreate(BaseModel):
    title: str
    description: str = None


class QualificationRead(BaseModel):
    id: int
    title: str
    description: Optional[str]


class QualificationUpdate(BaseModel):
    title: str = None
    description: str = None


class CoordsCreate(BaseModel):
    latitude: float
    longitude: float


class CoordsRead(BaseModel):
    id: int
    latitude: float
    longitude: float
    time_in: datetime.datetime


class CoordsUpdate(BaseModel):
    latitude: float = None
    longitude: float = None


class PolyclinicCreate(BaseModel):
    title: str
    description: str = None
    address: str


class PolyclinicRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    address: str


class PolyclinicUpdate(BaseModel):
    title: str = None
    description: str = None
    address: str = None


class DoctorCreate(BaseModel):
    first_name: str
    second_name: str
    last_name: str
    phone: str
    email: str
    specialization_id: int
    qualification_id: int
    polyclinic_id: int


class DoctorRead(BaseModel):
    id: int
    first_name: str
    second_name: str
    last_name: str
    phone: str
    email: str
    specialization_id: int
    qualification_id: int
    polyclinic_id: int


class DoctorUpdate(BaseModel):
    first_name: str = None
    second_name: str = None
    last_name: str = None
    phone: str = None
    email: str = None
    specialization_id: int = None
    qualification_id: int = None
    polyclinic_id: int = None


class PatientCreate(BaseModel):
    first_name: str
    second_name: str
    last_name: str
    phone: str
    email: str
    address: str
    polyclinic_id: int


class PatientRead(BaseModel):
    id: int
    first_name: str
    second_name: str
    last_name: str
    phone: str
    email: str
    address: str
    polyclinic_id: int


class PatientUpdate(BaseModel):
    first_name: str = None
    second_name: str = None
    last_name: str = None
    phone: str = None
    email: str = None
    address: str = None
    polyclinic_id: int = None


class RouteCreate(BaseModel):
    start_point: CoordsCreate
    finish_point: CoordsCreate
    doctor: int


class RouteRead(BaseModel):
    id: int
    start_point: CoordsRead
    finish_point: CoordsRead
    current_point: CoordsRead
    doctor: int
    route_active: bool


class RouteUpdate(BaseModel):
    current_point: CoordsUpdate = None
    route_active: bool = None
