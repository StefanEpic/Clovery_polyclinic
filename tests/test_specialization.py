from httpx import AsyncClient


async def test_add_one_specialization(ac: AsyncClient):
    response = await ac.post("/specializations", json={
        "title": "Ортопед"
    })

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_add_one_specialization_invalid_title_unique(ac: AsyncClient):
    response = await ac.post("/specializations", json={
        "title": "Ортопед"
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "UNIQUE constraint failed: specialization.title"


async def test_get_list_specializations(ac: AsyncClient):
    response = await ac.get("/specializations")

    assert response.status_code == 200
    assert response.json()[1]["id"] == 2
    assert len(response.json()) == 2
