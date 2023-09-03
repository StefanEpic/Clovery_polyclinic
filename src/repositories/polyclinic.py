from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from models.polyclinic import Specialization, Qualification, Coords, Polyclinic, Doctor, Patient, Route
from schemas.polyclinic import CoordsCreate, RouteRead, CoordsRead
from utils.repository import SQLAlchemyRepository


class SpecializationRepository(SQLAlchemyRepository):
    model = Specialization


class QualificationRepository(SQLAlchemyRepository):
    model = Qualification


class CoordsRepository(SQLAlchemyRepository):
    model = Coords


class PolyclinicRepository(SQLAlchemyRepository):
    model = Polyclinic


class DoctorRepository(SQLAlchemyRepository):
    model = Doctor


class PatientRepository(SQLAlchemyRepository):
    model = Patient


class RouteRepository(SQLAlchemyRepository):
    model = Route

    async def add_route(self, data):
        try:
            start_point = Coords(latitude=data.start_point.latitude, longitude=data.start_point.longitude)
            self.session.add(start_point)
            finish_point = Coords(latitude=data.finish_point.latitude, longitude=data.finish_point.longitude)
            self.session.add(finish_point)
            current_point = Coords(latitude=0, longitude=0)
            self.session.add(current_point)
            await self.session.commit()
            await self.session.refresh(start_point)
            await self.session.refresh(finish_point)
            await self.session.refresh(current_point)
            route = Route(start_point=start_point.id,
                          finish_point=finish_point.id,
                          current_point=current_point.id,
                          doctor=data.doctor)
            self.session.add(route)
            await self.session.commit()
            await self.session.refresh(route)
            return RouteRead(id=route.id,
                             start_point=start_point.to_read_model(),
                             finish_point=finish_point.to_read_model(),
                             current_point=current_point.to_read_model(),
                             doctor=route.doctor,
                             route_active=route.route_active)
        except ValueError as e:
            raise HTTPException(status_code=200, detail=str(e))
        except IntegrityError as e:
            raise HTTPException(status_code=200, detail=str(e.orig))

    async def edit_route(self, self_id: int, data):
        try:
            res = await self.session.get(self.model, self_id)
            if not res:
                raise HTTPException(status_code=404, detail="Not found")

            if data.current_point:
                current_point = await self.session.get(Coords, res.current_point)
                point_data = data.current_point.dict(exclude_unset=True)
                for key, value in point_data.items():
                    setattr(current_point, key, value)
                self.session.add(current_point)
                await self.session.commit()

            res_data = data.dict(exclude_unset=True)
            for key, value in res_data.items():
                if key != 'current_point':
                    setattr(res, key, value)
            self.session.add(res)
            await self.session.commit()
            await self.session.refresh(res)

            start_point = await self.session.get(Coords, res.start_point)
            finish_point = await self.session.get(Coords, res.finish_point)

            return RouteRead(id=res.id,
                             start_point=start_point.to_read_model(),
                             finish_point=finish_point.to_read_model(),
                             current_point=current_point.to_read_model(),
                             doctor=res.doctor,
                             route_active=res.route_active)
        except ValueError as e:
            raise HTTPException(status_code=200, detail=str(e))
