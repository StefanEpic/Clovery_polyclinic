from api.polyclinic.coords import router as router_coords
from api.polyclinic.doctor import router as router_doctor
from api.polyclinic.patient import router as router_patient
from api.polyclinic.polyclinic import router as router_polyclinic
from api.polyclinic.qualification import router as router_qualification
from api.polyclinic.route import router as router_route
from api.polyclinic.specialization import router as router_specialization

all_routers = [
    router_coords,
    router_doctor,
    router_patient,
    router_polyclinic,
    router_qualification,
    router_route,
    router_specialization
]
