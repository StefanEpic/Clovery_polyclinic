from httpx import AsyncClient


async def test_add_one_doctor(ac: AsyncClient):
    response = await ac.post("/doctors", json={
        "first_name": "Борис",
        "second_name": "Борисов",
        "last_name": "Борисович",
        "phone": "+88888888888",
        "email": "boris@test.com",
        "address": 'ул. Пушкин, д. 15',
        "specialization_id": 1,
        "qualification_id": 1,
        "polyclinic_id": 1
    })

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_add_one_doctor_invalid_polyclinic(ac: AsyncClient):
    response = await ac.post("/doctors", json={
        "first_name": "Борис",
        "second_name": "Борисов",
        "last_name": "Борисович",
        "phone": "+88888888888",
        "email": "boris@test.com",
        "address": 'ул. Пушкин, д. 15',
        "specialization_id": 1,
        "qualification_id": 1,
        "polyclinic_id": 55
    })

    assert response.status_code == 404
    assert response.json()["detail"] == 'Polyclinic with this id not found'


async def test_add_one_doctor_invalid_qualification(ac: AsyncClient):
    response = await ac.post("/doctors", json={
        "first_name": "Борис",
        "second_name": "Борисов",
        "last_name": "Борисович",
        "phone": "+88888888888",
        "email": "boris@test.com",
        "address": 'ул. Пушкин, д. 15',
        "specialization_id": 1,
        "qualification_id": 55,
        "polyclinic_id": 1
    })

    assert response.status_code == 404
    assert response.json()["detail"] == 'Qualification with this id not found'


async def test_add_one_doctor_invalid_specialization(ac: AsyncClient):
    response = await ac.post("/doctors", json={
        "first_name": "Борис",
        "second_name": "Борисов",
        "last_name": "Борисович",
        "phone": "+88888888888",
        "email": "boris@test.com",
        "address": 'ул. Пушкин, д. 15',
        "specialization_id": 55,
        "qualification_id": 1,
        "polyclinic_id": 1
    })

    assert response.status_code == 404
    assert response.json()["detail"] == 'Specialization with this id not found'


async def test_add_one_doctor_invalid_name(ac: AsyncClient):
    response = await ac.post("/doctors", json={
        "first_name": "Борис333",
        "second_name": "Борисов",
        "last_name": "Борисович",
        "phone": "+88888888888",
        "email": "boris@test.com",
        "address": 'ул. Пушкин, д. 15',
        "specialization_id": 1,
        "qualification_id": 1,
        "polyclinic_id": 1
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "Error. Invalid value for name field"


async def test_add_one_doctor_invalid_phone_unique(ac: AsyncClient):
    response = await ac.post("/doctors", json={
        "first_name": "Борис",
        "second_name": "Борисов",
        "last_name": "Борисович",
        "phone": "+88888888888",
        "email": "boris3@test.com",
        "address": 'ул. Пушкин, д. 15',
        "specialization_id": 1,
        "qualification_id": 1,
        "polyclinic_id": 1
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "UNIQUE constraint failed: doctor.phone"


async def test_add_one_doctor_invalid_phone_text(ac: AsyncClient):
    response = await ac.post("/doctors", json={
        "first_name": "Борис",
        "second_name": "Борисов",
        "last_name": "Борисович",
        "phone": "asd",
        "email": "boris@test.com",
        "address": 'ул. Пушкин, д. 15',
        "specialization_id": 1,
        "qualification_id": 1,
        "polyclinic_id": 1
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "Error. Invalid value for phone field"


async def test_add_one_doctor_invalid_email_unique(ac: AsyncClient):
    response = await ac.post("/doctors", json={
        "first_name": "Борис",
        "second_name": "Борисов",
        "last_name": "Борисович",
        "phone": "+88888888889",
        "email": "boris@test.com",
        "address": 'ул. Пушкин, д. 15',
        "specialization_id": 1,
        "qualification_id": 1,
        "polyclinic_id": 1
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "UNIQUE constraint failed: doctor.email"


async def test_add_one_doctor_invalid_email_symbols(ac: AsyncClient):
    response = await ac.post("/doctors", json={
        "first_name": "Борис",
        "second_name": "Борисов",
        "last_name": "Борисович",
        "phone": "+88888888889",
        "email": "boris",
        "address": 'ул. Пушкин, д. 15',
        "specialization_id": 1,
        "qualification_id": 1,
        "polyclinic_id": 1
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "Error. Invalid value for email field"


async def test_get_list_doctors(ac: AsyncClient):
    response = await ac.get("/doctors")

    assert response.status_code == 200
    assert response.json()[1]["id"] == 2
    assert len(response.json()) == 2


async def test_get_list_doctors_with_filter(ac: AsyncClient):
    response = await ac.get("/doctors", params={
        "phone": "+88888888888",
        "email": "boris@test.com"
    })

    assert response.status_code == 200
    assert response.json()[0]["id"] == 2
    assert len(response.json()) == 1


async def test_get_one_doctor(ac: AsyncClient):
    response = await ac.get("/doctors/2")

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_get_one_doctor_route(ac: AsyncClient):
    response = await ac.get("/doctors/1/route")

    assert response.status_code == 200
    assert response.json()["start_point"]["latitude"] == 5
    assert response.json()["start_point"]["longitude"] == 5
    assert response.json()["id"] == 1


async def test_edit_one_doctor(ac: AsyncClient):
    response = await ac.patch("/doctors/2", json={"first_name": "Виктор"})

    assert response.status_code == 200
    assert response.json()["first_name"] == "Виктор"
    assert response.json()["id"] == 2


async def test_edit_one_doctor_invalid_polyclinic(ac: AsyncClient):
    response = await ac.patch("/doctors/2", json={"polyclinic_id": "55"})

    assert response.status_code == 404
    assert response.json()["detail"] == 'Polyclinic with this id not found'


async def test_delete_one_doctor(ac: AsyncClient):
    response = await ac.delete("/doctors/2")

    assert response.status_code == 200
    assert response.json()["detail"] == "success"
