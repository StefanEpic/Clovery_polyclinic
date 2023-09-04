from httpx import AsyncClient


async def test_add_one_coords(ac: AsyncClient):
    response = await ac.post("/coords", json={
        "latitude": 15.15,
        "longitude": 16.16
    })

    assert response.status_code == 200
    assert response.json()["id"] == 4


async def test_get_list_coordss(ac: AsyncClient):
    response = await ac.get("/coords")

    assert response.status_code == 200
    assert response.json()[3]["id"] == 4
    assert len(response.json()) == 4


async def test_get_one_coords(ac: AsyncClient):
    response = await ac.get("/coords/4")

    assert response.status_code == 200
    assert response.json()["id"] == 4


async def test_edit_one_coords(ac: AsyncClient):
    response = await ac.patch("/coords/4", json={"longitude": 17.17})

    assert response.status_code == 200
    assert response.json()["longitude"] == 17.17
    assert response.json()["id"] == 4


async def test_delete_one_coords(ac: AsyncClient):
    response = await ac.delete("/coords/4")

    assert response.status_code == 200
    assert response.json()["detail"] == "success"
