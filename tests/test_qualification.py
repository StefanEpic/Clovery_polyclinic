from httpx import AsyncClient


async def test_add_one_qualification(ac: AsyncClient):
    response = await ac.post("/qualifications", json={
        "title": "Первая"
    })

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_add_one_qualification_invalid_title(ac: AsyncClient):
    response = await ac.post("/qualifications", json={
        "title": "Первая123"
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "Error. Invalid value for name field"


async def test_add_one_qualification_invalid_title_unique(ac: AsyncClient):
    response = await ac.post("/qualifications", json={
        "title": "Первая"
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "UNIQUE constraint failed: qualification.title"


async def test_get_list_qualifications(ac: AsyncClient):
    response = await ac.get("/qualifications")

    assert response.status_code == 200
    assert response.json()[1]["id"] == 2
    assert len(response.json()) == 2


async def test_get_one_qualification(ac: AsyncClient):
    response = await ac.get("/qualifications/2")

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_edit_one_qualification(ac: AsyncClient):
    response = await ac.patch("/qualifications/2", json={"title": "Вторая"})

    assert response.status_code == 200
    assert response.json()["title"] == "Вторая"
    assert response.json()["id"] == 2


async def test_delete_one_qualification(ac: AsyncClient):
    response = await ac.delete("/qualifications/2")

    assert response.status_code == 200
    assert response.json()["detail"] == "success"
