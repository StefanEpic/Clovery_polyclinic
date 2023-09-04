from httpx import AsyncClient


async def test_add_one_patient(ac: AsyncClient):
    response = await ac.post("/patients", json={
        "first_name": "Борис",
        "second_name": "Борисов",
        "last_name": "Борисович",
        "phone": "+88888888888",
        "email": "boris@test.com",
        "address": 'ул. Пушкин, д. 15',
        "polyclinic_id": 1
    })

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_add_one_patient_invalid_polyclinic(ac: AsyncClient):
    response = await ac.post("/patients", json={
        "first_name": "Борис",
        "second_name": "Борисов",
        "last_name": "Борисович",
        "phone": "+88888888888",
        "email": "boris@test.com",
        "address": 'ул. Пушкин, д. 15',
        "polyclinic_id": 55
    })

    assert response.status_code == 404
    assert response.json()["detail"] == 'Polyclinic with this id not found'


async def test_add_one_patient_invalid_name(ac: AsyncClient):
    response = await ac.post("/patients", json={
        "first_name": "Борис333",
        "second_name": "Борисов",
        "last_name": "Борисович",
        "phone": "+88888888888",
        "email": "boris@test.com",
        "address": 'ул. Пушкин, д. 15',
        "polyclinic_id": 1
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "Error. Invalid value for name field"


async def test_add_one_patient_invalid_phone_unique(ac: AsyncClient):
    response = await ac.post("/patients", json={
        "first_name": "Борис",
        "second_name": "Борисов",
        "last_name": "Борисович",
        "phone": "+88888888888",
        "email": "boris5@test.com",
        "address": 'ул. Пушкин, д. 15',
        "polyclinic_id": 1
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "UNIQUE constraint failed: patient.phone"


async def test_add_one_patient_invalid_phone_text(ac: AsyncClient):
    response = await ac.post("/patients", json={
        "first_name": "Борис",
        "second_name": "Борисов",
        "last_name": "Борисович",
        "phone": "asd",
        "email": "boris@test.com",
        "address": 'ул. Пушкин, д. 15',
        "polyclinic_id": 1
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "Error. Invalid value for phone field"


async def test_add_one_patient_invalid_email_unique(ac: AsyncClient):
    response = await ac.post("/patients", json={
        "first_name": "Борис",
        "second_name": "Борисов",
        "last_name": "Борисович",
        "phone": "+88888888889",
        "email": "boris@test.com",
        "address": 'ул. Пушкин, д. 15',
        "polyclinic_id": 1
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "UNIQUE constraint failed: patient.email"


async def test_add_one_patient_invalid_email_symbols(ac: AsyncClient):
    response = await ac.post("/patients", json={
        "first_name": "Борис",
        "second_name": "Борисов",
        "last_name": "Борисович",
        "phone": "+88888888889",
        "email": "boris",
        "address": 'ул. Пушкин, д. 15',
        "polyclinic_id": 1
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "Error. Invalid value for email field"


async def test_get_list_patients(ac: AsyncClient):
    response = await ac.get("/patients")

    assert response.status_code == 200
    assert response.json()[1]["id"] == 2
    assert len(response.json()) == 2


async def test_get_list_patients_with_filter(ac: AsyncClient):
    response = await ac.get("/patients", params={
        "phone": "+88888888888",
        "email": "boris@test.com"
    })

    assert response.status_code == 200
    assert response.json()[0]["id"] == 2
    assert len(response.json()) == 1


async def test_get_one_patient(ac: AsyncClient):
    response = await ac.get("/patients/2")

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_edit_one_patient(ac: AsyncClient):
    response = await ac.patch("/patients/2", json={"first_name": "Виктор"})

    assert response.status_code == 200
    assert response.json()["first_name"] == "Виктор"
    assert response.json()["id"] == 2


async def test_edit_one_patient_invalid_polyclinic(ac: AsyncClient):
    response = await ac.patch("/patients/2", json={"polyclinic_id": "55"})

    assert response.status_code == 404
    assert response.json()["detail"] == 'Polyclinic with this id not found'


async def test_delete_one_patient(ac: AsyncClient):
    response = await ac.delete("/patients/2")

    assert response.status_code == 200
    assert response.json()["detail"] == "success"
