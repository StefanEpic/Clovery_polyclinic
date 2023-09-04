from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from models.polyclinic import Specialization, Qualification, Coords, Polyclinic, Doctor, Patient, Route
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

        stmt = select(Route).where(Route.doctor_id == self_id)
        route = await self.session.execute(stmt)
        route = route.scalars().first()
        print("!@#@!#!@#@!#@!#!@")
        print(route)

        if route:
            start_point = await self.session.get(Coords, route.start_point)
            finish_point = await self.session.get(Coords, route.finish_point)
            current_point = await self.session.get(Coords, route.current_point)
            print(start_point)
            print(finish_point)
            print(current_point)

            route = route.to_read_model(start_point.to_read_model(),
                                        finish_point.to_read_model(),
                                        current_point.to_read_model()
                                        )
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
                          doctor_id=data.doctor_id)
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
                point_data = data.current_point.model_dump(exclude_unset=True)
                for key, value in point_data.items():
                    setattr(current_point, key, value)
                self.session.add(current_point)
                await self.session.commit()

            if data.route_active is not None:
                res.route_active = data.route_active
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
