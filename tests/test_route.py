from httpx import AsyncClient


async def test_add_one_route(ac: AsyncClient):
    response = await ac.post("/routes", json={
        "start_point": {
            "latitude": 30,
            "longitude": 30
        },
        "finish_point": {
            "latitude": 50,
            "longitude": 50
        },
        "doctor_id": 1
    })

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_add_one_route_invalid_doctor(ac: AsyncClient):
    response = await ac.post("/routes", json={
        "start_point": {
            "latitude": 30,
            "longitude": 30
        },
        "finish_point": {
            "latitude": 50,
            "longitude": 50
        },
        "doctor_id": 55
    })

    assert response.status_code == 404
    assert response.json()["detail"] == 'Doctor with this id not found'


async def test_get_list_routes(ac: AsyncClient):
    response = await ac.get("/routes")

    assert response.status_code == 200
    assert response.json()[1]["id"] == 2
    assert len(response.json()) == 2


async def test_get_one_route(ac: AsyncClient):
    response = await ac.get("/routes/2")

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_edit_one_route(ac: AsyncClient):
    response = await ac.patch("/routes/2", json={
        "current_point": {
            "latitude": 40,
            "longitude": 40
        }
    })

    assert response.status_code == 200
    assert response.json()["current_point"]["latitude"] == 40
    assert response.json()["current_point"]["longitude"] == 40
    assert response.json()["id"] == 2


async def test_edit_one_route_status(ac: AsyncClient):
    response = await ac.patch("/routes/2", json={"route_active": False})

    assert response.status_code == 200
    assert response.json()["route_active"] == False
    assert response.json()["id"] == 2


async def test_delete_one_route(ac: AsyncClient):
    response = await ac.delete("/routes/2")

    assert response.status_code == 200
    assert response.json()["detail"] == "success"
