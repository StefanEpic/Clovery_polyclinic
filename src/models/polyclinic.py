import datetime
from typing import Optional, List

from sqlalchemy import String, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase, validates

from schemas.polyclinic import CoordsRead, RouteRead
from utils.validators import name_valid, phone_valid, email_valid


class Base(DeclarativeBase):
    pass


class Specialization(Base):
    __tablename__ = "specialization"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    doctors: Mapped[Optional[List["Doctor"]]] = relationship(back_populates="specialization")

    @validates("title")
    def validate_name(self, key, title):
        return name_valid(title)


class Qualification(Base):
    __tablename__ = "qualification"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    doctors: Mapped[Optional[List["Doctor"]]] = relationship(back_populates="qualification")

    @validates("title")
    def validate_name(self, key, title):
        return name_valid(title)


class Coords(Base):
    __tablename__ = "coords"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    latitude: Mapped[float]
    longitude: Mapped[float]
    time_in: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)

    def to_read_model(self) -> CoordsRead:
        return CoordsRead(
            id=self.id,
            latitude=self.latitude,
            longitude=self.longitude,
            time_in=self.time_in
        )


class Polyclinic(Base):
    __tablename__ = "polyclinic"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(String(255))
    doctors: Mapped[List["Doctor"]] = relationship(back_populates="polyclinic")
    patients: Mapped[List["Patient"]] = relationship(back_populates="polyclinic")


class Doctor(Base):
    __tablename__ = "doctor"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100))
    second_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(12), unique=True)
    email: Mapped[str] = mapped_column(String(30), unique=True)

    specialization_id: Mapped[int] = mapped_column(ForeignKey("specialization.id"))
    specialization: Mapped["Specialization"] = relationship(back_populates="doctors")
    qualification_id: Mapped[int] = mapped_column(ForeignKey("qualification.id"))
    qualification: Mapped["Qualification"] = relationship(back_populates="doctors")
    polyclinic_id: Mapped[int] = mapped_column(ForeignKey("polyclinic.id"))
    polyclinic: Mapped["Polyclinic"] = relationship(back_populates="doctors")

    @validates("first_name", "second_name", "last_name")
    def validate_name(self, key, *names):
        for name in names:
            return name_valid(name)

    @validates("phone")
    def validate_phone(self, key, phone):
        return phone_valid(phone)

    @validates("email")
    def validate_email(self, key, email):
        return email_valid(email)


class Patient(Base):
    __tablename__ = "patient"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100))
    second_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(12), unique=True)
    email: Mapped[str] = mapped_column(String(30), unique=True)
    address: Mapped[str] = mapped_column(String(255))

    polyclinic_id: Mapped[int] = mapped_column(ForeignKey("polyclinic.id"))
    polyclinic: Mapped["Polyclinic"] = relationship(back_populates="patients")

    @validates("first_name", "second_name", "last_name")
    def validate_name(self, key, *names):
        for name in names:
            return name_valid(name)

    @validates("phone")
    def validate_phone(self, key, phone):
        return phone_valid(phone)

    @validates("email")
    def validate_email(self, key, email):
        return email_valid(email)


class Route(Base):
    __tablename__ = "route"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    start_point: Mapped[int] = mapped_column(ForeignKey("coords.id"))
    finish_point: Mapped[int] = mapped_column(ForeignKey("coords.id"))
    current_point: Mapped[Optional[int]] = mapped_column(ForeignKey("coords.id"))
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctor.id"))
    route_active: Mapped[bool] = mapped_column(default=True)

    idx_doctor_id = Index('idx_doctor_id', doctor_id)

    def to_read_model(self, start_point, finish_point, current_point) -> RouteRead:
        return RouteRead(
            id=self.id,
            start_point=start_point,
            finish_point=finish_point,
            current_point=current_point,
            doctor_id=self.doctor_id,
            route_active=self.route_active
        )
