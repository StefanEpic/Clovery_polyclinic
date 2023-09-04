from httpx import AsyncClient


async def test_add_one_polyclinic(ac: AsyncClient):
    response = await ac.post("/polyclinics", json={
        "title": "Поликлиника №2",
        "address": "Прямая ул., д. 2"
    })

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_add_one_polyclinic_invalid_title_unique(ac: AsyncClient):
    response = await ac.post("/polyclinics", json={
        "title": "Поликлиника №2",
        "address": "Прямая ул., д. 2"
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "UNIQUE constraint failed: polyclinic.title"


async def test_get_list_polyclinics(ac: AsyncClient):
    response = await ac.get("/polyclinics")

    assert response.status_code == 200
    assert response.json()[1]["id"] == 2
    assert len(response.json()) == 2


async def test_get_one_polyclinic(ac: AsyncClient):
    response = await ac.get("/polyclinics/2")

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_edit_one_polyclinic(ac: AsyncClient):
    response = await ac.patch("/polyclinics/2", json={"title": "Поликлиника №5"})

    assert response.status_code == 200
    assert response.json()["title"] == "Поликлиника №5"
    assert response.json()["id"] == 2


async def test_delete_one_polyclinic(ac: AsyncClient):
    response = await ac.delete("/polyclinics/2")

    assert response.status_code == 200
    assert response.json()["detail"] == "success"
