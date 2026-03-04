import uuid

import pytest
from fastapi import status
from httpx import AsyncClient

from app.exceptions.business import TicketNotFoundError

url_base = "/tickets"


async def test_create_ticket(aclient: AsyncClient) -> None:
    response = await aclient.post(
        url_base,
        json={
            "title": "Naruto",
            "description": "Naruto Shippuden with Sasuke",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Naruto"
    assert data["description"] == "Naruto Shippuden with Sasuke"
    assert data["status"] == "open"
    assert "id" in data
    assert "created_at" in data


async def test_create_ticket_with_different_status(aclient: AsyncClient) -> None:
    response = await aclient.post(
        url_base,
        json={"title": "Naruto & Sakura", "description": "Naruto Shippuden with Sakura", "status": "closed"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Naruto & Sakura"
    assert data["description"] == "Naruto Shippuden with Sakura"
    assert data["status"] == "closed"
    assert "id" in data
    assert "created_at" in data


async def test_create_ticket_missing_title(aclient: AsyncClient) -> None:
    response = await aclient.post(
        url_base,
        json={
            "description": "Naruto Shippuden n'a pas de tête",
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


async def test_get_tickets(aclient: AsyncClient) -> None:
    await aclient.post(url_base, json={"title": "Ticket 1", "description": "Desc 1"})
    await aclient.post(url_base, json={"title": "Ticket 2", "description": "Desc 2"})
    response = await aclient.get(url_base)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2


async def test_get_ticket_by_id(aclient: AsyncClient) -> None:
    created = await aclient.post(url_base, json={"title": "Bug", "description": "Desc"})
    ticket_id = created.json()["id"]

    response = await aclient.get(f"{url_base}/{ticket_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == ticket_id


async def test_get_ticket_not_found(aclient: AsyncClient) -> None:
    with pytest.raises(TicketNotFoundError):
        await aclient.get(f"{url_base}/{uuid.uuid4()}")


async def test_update_ticket(aclient: AsyncClient) -> None:
    created = await aclient.post(
        f"{url_base}", json={"title": "Demons slayer", "description": "Demons slayer Description"}
    )
    ticket_id = created.json()["id"]
    new_title = "Demons slayer saison 2"
    response = await aclient.put(f"{url_base}/{ticket_id}", json={"title": new_title})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == new_title
    assert response.json()["description"] == "Demons slayer Description"


async def test_close_ticket(aclient: AsyncClient) -> None:
    created = await aclient.post(
        f"{url_base}", json={"title": "Demons slayer", "description": "Demons slayer Description"}
    )
    ticket_id = created.json()["id"]
    assert created.json()["status"] == "open"
    response = await aclient.patch(f"{url_base}/{ticket_id}/close")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "closed"
