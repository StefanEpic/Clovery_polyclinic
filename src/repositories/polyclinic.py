from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from models.polyclinic import Specialization, Qualification, Coords, Polyclinic, Doctor, Patient, Route
from schemas.polyclinic import RouteRead
from utils.repository import SQLAlchemyRepository, UserFilterRepository


class SpecializationRepository(SQLAlchemyRepository):
    model = Specialization


class QualificationRepository(SQLAlchemyRepository):
    model = Qualification


class CoordsRepository(SQLAlchemyRepository):
    model = Coords


class PolyclinicRepository(SQLAlchemyRepository):
    model = Polyclinic


class DoctorRepository(UserFilterRepository):
    model = Doctor

    async def get_doctor_route(self, self_id: int):
        res = await self.session.get(self.model, self_id)
        if not res:
            raise HTTPException(status_code=404, detail="Not found")

        stmt = select(Route).where(Route.doctor == self_id)
        route = await self.session.execute(stmt)
        route = route.scalars().first()

        start_point = await self.session.get(Coords, route.start_point)
        finish_point = await self.session.get(Coords, route.finish_point)
        current_point = await self.session.get(Coords, route.current_point)

        if route:
            route = RouteRead(id=route.id,
                              start_point=start_point.to_read_model(),
                              finish_point=finish_point.to_read_model(),
                              current_point=current_point.to_read_model(),
                              doctor=route.doctor,
                              route_active=route.route_active)

        return route


class PatientRepository(UserFilterRepository):
    model = Patient


class RouteRepository(SQLAlchemyRepository):
    model = Route

    async def get_route(self, self_id: int):
        res = await self.session.get(self.model, self_id)
        if not res:
            raise HTTPException(status_code=404, detail="Not found")

        start_point = await self.session.get(Coords, res.start_point)
        finish_point = await self.session.get(Coords, res.finish_point)
        current_point = await self.session.get(Coords, res.current_point)

        return res.to_read_model(start_point.to_read_model(),
                                 finish_point.to_read_model(),
                                 current_point.to_read_model()
                                 )

    async def add_route(self, data):
        try:
            doctor = await self.session.get(Doctor, data.doctor)
            if not doctor:
                raise HTTPException(status_code=404, detail="Doctor with this id not found")

            start_point = Coords(latitude=data.start_point.latitude, longitude=data.start_point.longitude)
            finish_point = Coords(latitude=data.finish_point.latitude, longitude=data.finish_point.longitude)
            current_point = Coords(latitude=0, longitude=0)
            self.session.add(start_point)
            self.session.add(finish_point)
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
            return route.to_read_model(start_point.to_read_model(),
                                       finish_point.to_read_model(),
                                       current_point.to_read_model()
                                       )
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

            res_data = data.model_dump(exclude_unset=True)
            for key, value in res_data.items():
                if key != 'current_point':
                    setattr(res, key, value)
            self.session.add(res)
            await self.session.commit()
            await self.session.refresh(res)

            start_point = await self.session.get(Coords, res.start_point)
            finish_point = await self.session.get(Coords, res.finish_point)
            current_point = await self.session.get(Coords, res.current_point)

            return res.to_read_model(start_point.to_read_model(),
                                     finish_point.to_read_model(),
                                     current_point.to_read_model()
                                     )
        except ValueError as e:
            raise HTTPException(status_code=200, detail=str(e))

    async def delete_route(self, self_id: int):
        res = await self.session.get(self.model, self_id)
        if not res:
            raise HTTPException(status_code=404, detail="Not found")
        start_point = await self.session.get(Coords, res.start_point)
        finish_point = await self.session.get(Coords, res.finish_point)
        current_point = await self.session.get(Coords, res.current_point)
        await self.session.delete(res)
        await self.session.delete(start_point)
        await self.session.delete(finish_point)
        await self.session.delete(current_point)
        await self.session.commit()
        return {"detail": "success"}
