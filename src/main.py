from fastapi import FastAPI

from api.routers import all_routers

app = FastAPI(title="Cloveri Polyclinic")

for router in all_routers:
    app.include_router(router)
