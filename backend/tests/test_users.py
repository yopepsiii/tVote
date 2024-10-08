import uuid

import pytest

from backend.app import models


def test_get_me(authorized_client, test_user, fastapi_cache):
    res = authorized_client.get("/users/me")
    assert res.status_code == 200
    user_info = res.json()
    assert user_info["email"] == test_user["email"]
    assert user_info["firstname"] == test_user["firstname"]
    assert user_info["surname"] == test_user["surname"]


def test_get_me_unauthorized(client):
    res = client.get("/users/me")
    assert res.status_code == 401


def test_get_users(admin_client, fastapi_cache):
    res = admin_client.get("/users")

    assert res.status_code == 200
    assert models.User(**res.json()[0])


def test_get_users_owner(owner_client, fastapi_cache):
    res = owner_client.get("/users")

    assert res.status_code == 200
    assert models.User(**res.json()[0])


def test_get_users_user(authorized_client, fastapi_cache):
    res = authorized_client.get("/users")
    assert res.status_code == 403


def test_get_users_unauthorized(client, fastapi_cache):
    res = client.get("/users")
    assert res.status_code == 401


def test_search_users(admin_client, fastapi_cache):
    res = admin_client.get("/users/search?query=test")
    assert res.status_code == 200

    users = res.json()
    assert models.User(**users[0])


def test_search_users_owner(owner_client, fastapi_cache):
    res = owner_client.get("/users/search?query=test")
    assert res.status_code == 200

    users = res.json()
    assert models.User(**users[0])


def test_search_users_client(authorized_client, fastapi_cache):
    res = authorized_client.get("/users/search?query=test")
    assert res.status_code == 403


@pytest.mark.asyncio
async def test_search_users_unauthorized(client, fastapi_cache):
    res = client.get("/users/search?query=test")
    assert res.status_code == 401


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "firstname, surname, email, password, status",
    [
        ("test", "test", "test@test.com", "test", 201),
        (None, "test", "test@test.com", "test", 422),
        (None, None, "test@test.com", "test", 422),
        (None, None, None, "test", 422),
        (None, None, None, None, 422),
    ],
)
async def test_create_user(
    admin_client, firstname, surname, email, password, status, fastapi_cache
):
    res = admin_client.post(
        "/users",
        json={
            "firstname": firstname,
            "surname": surname,
            "email": email,
            "password": password,
        },
    )
    assert res.status_code == status
    if status == 201:
        new_user = res.json()

        assert new_user["firstname"] == firstname
        assert new_user["surname"] == surname
        assert new_user["email"] == email


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "firstname, surname, email, password, status",
    [
        ("test", "test", "test@test.com", "test", 201),
        (None, "test", "test@test.com", "test", 422),
        (None, None, "test@test.com", "test", 422),
        (None, None, None, "test", 422),
        (None, None, None, None, 422),
    ],
)
async def test_create_user_owner(
    owner_client, firstname, surname, email, password, status, fastapi_cache
):
    res = owner_client.post(
        "/users",
        json={
            "firstname": firstname,
            "surname": surname,
            "email": email,
            "password": password,
        },
    )
    assert res.status_code == status
    if status == 201:
        new_user = res.json()

        assert new_user["firstname"] == firstname
        assert new_user["surname"] == surname
        assert new_user["email"] == email


@pytest.mark.parametrize(
    "firstname, surname, email, password",
    [
        ("test", "test", "test@test.com", "test"),
        (None, "test", "test@test.com", "test"),
        (None, None, "test@test.com", "test"),
        (None, None, None, "test"),
        (None, None, None, None),
    ],
)
def test_create_user_user(
    authorized_client, firstname, surname, email, password, fastapi_cache
):
    res = authorized_client.post(
        "/users",
        json={
            "firstname": firstname,
            "surname": surname,
            "email": email,
            "password": password,
        },
    )
    assert res.status_code == 403


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "firstname, surname, email, password",
    [
        ("test", "test", "test@test.com", "test"),
        (None, "test", "test@test.com", "test"),
        (None, None, "test@test.com", "test"),
        (None, None, None, "test"),
        (None, None, None, None),
    ],
)
async def test_create_user_unauthorized(
    client, firstname, surname, email, password, fastapi_cache
):
    res = client.post(
        "/users",
        json={
            "firstname": firstname,
            "surname": surname,
            "email": email,
            "password": password,
        },
    )
    assert res.status_code == 401


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "firstname, surname, email, password",
    [
        ("new_test", "new_test", "new_test@test.com", "new_test"),
        (None, "new_test", "new_test@test.com", "new_test"),
        (None, None, "new_test@test.com", "new_test"),
        (None, None, None, "new_test"),
        (None, None, None, None),
    ],
)
async def test_update_user(
    admin_client, test_user, firstname, surname, email, password, fastapi_cache
):
    data = {
        "firstname": firstname,
        "surname": surname,
        "email": email,
        "password": password,
    }
    update_data = {k: v for k, v in data.items() if v is not None}

    res = admin_client.patch(f"/users/{test_user['id']}", json=update_data)

    assert res.status_code == 200

    updated_user = res.json()

    if update_data.get("firstname"):
        assert updated_user["firstname"] == update_data["firstname"]
    if update_data.get("surname"):
        assert updated_user["surname"] == update_data["surname"]
    if update_data.get("email"):
        assert updated_user["email"] == update_data["email"]
    if update_data.get("password"):
        assert updated_user["password"] == update_data["password"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "firstname, surname, email, password",
    [
        ("new_test", "new_test", "new_test@test.com", "new_test"),
        (None, "new_test", "new_test@test.com", "new_test"),
        (None, None, "new_test@test.com", "new_test"),
        (None, None, None, "new_test"),
        (None, None, None, None),
    ],
)
async def test_update_admin(
    admin_client, test_admin2, firstname, surname, email, password, fastapi_cache
):
    data = {
        "firstname": firstname,
        "surname": surname,
        "email": email,
        "password": password,
    }
    update_data = {k: v for k, v in data.items() if v is not None}

    res = admin_client.patch(f"/users/{test_admin2['id']}", json=update_data)

    assert res.status_code == 403


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "firstname, surname, email, password",
    [
        ("new_test", "new_test", "new_test@test.com", "new_test"),
        (None, "new_test", "new_test@test.com", "new_test"),
        (None, None, "new_test@test.com", "new_test"),
        (None, None, None, "new_test"),
        (None, None, None, None),
    ],
)
async def test_update_owner(
    admin_client, test_owner, firstname, surname, email, password, fastapi_cache
):
    data = {
        "firstname": firstname,
        "surname": surname,
        "email": email,
        "password": password,
    }
    update_data = {k: v for k, v in data.items() if v is not None}

    res = admin_client.patch(f"/users/{test_owner['id']}", json=update_data)

    assert res.status_code == 403


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "firstname, surname, email, password",
    [
        ("new_test", "new_test", "new_test@test.com", "new_test"),
        (None, "new_test", "new_test@test.com", "new_test"),
        (None, None, "new_test@test.com", "new_test"),
        (None, None, None, "new_test"),
        (None, None, None, None),
    ],
)
async def test_update_user_owner(
    owner_client, test_user, firstname, surname, email, password, fastapi_cache
):
    data = {
        "firstname": firstname,
        "surname": surname,
        "email": email,
        "password": password,
    }
    update_data = {k: v for k, v in data.items() if v is not None}

    res = owner_client.patch(f"/users/{test_user['id']}", json=update_data)

    assert res.status_code == 200

    updated_user = res.json()

    if update_data.get("firstname"):
        assert updated_user["firstname"] == update_data["firstname"]
    if update_data.get("surname"):
        assert updated_user["surname"] == update_data["surname"]
    if update_data.get("email"):
        assert updated_user["email"] == update_data["email"]
    if update_data.get("password"):
        assert updated_user["password"] == update_data["password"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "firstname, surname, email, password",
    [
        ("new_test", "new_test", "new_test@test.com", "new_test"),
        (None, "new_test", "new_test@test.com", "new_test"),
        (None, None, "new_test@test.com", "new_test"),
        (None, None, None, "new_test"),
        (None, None, None, None),
    ],
)
async def test_update_user_user(
    authorized_client, test_user, firstname, surname, email, password, fastapi_cache
):
    data = {
        "firstname": firstname,
        "surname": surname,
        "email": email,
        "password": password,
    }
    update_data = {k: v for k, v in data.items() if v is not None}

    res = authorized_client.patch(f"/users/{test_user['id']}", json=update_data)

    assert res.status_code == 403


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "firstname, surname, email, password",
    [
        ("new_test", "new_test", "new_test@test.com", "new_test"),
        (None, "new_test", "new_test@test.com", "new_test"),
        (None, None, "new_test@test.com", "new_test"),
        (None, None, None, "new_test"),
        (None, None, None, None),
    ],
)
async def test_update_user_unauthorized(
    client, test_user, firstname, surname, email, password, fastapi_cache
):
    data = {
        "firstname": firstname,
        "surname": surname,
        "email": email,
        "password": password,
    }
    update_data = {k: v for k, v in data.items() if v is not None}

    res = client.patch(f"/users/{test_user['id']}", json=update_data)

    assert res.status_code == 401


def test_update_user_wrong_id(admin_client):
    data = {
        "firstname": "firstname",
        "surname": "surname",
        "email": "email@test.com",
        "password": "password",
    }
    res = admin_client.patch(f"/users/{uuid.uuid4()}", json=data)

    assert res.status_code == 404


def test_delete_user_owner(owner_client, test_admin2):
    res = owner_client.delete(f"/users/{test_admin2['id']}")
    assert res.status_code == 204


def test_delete_user_admin(admin_client, test_owner, test_user):
    res = admin_client.delete(f"/users/{test_owner['id']}")
    assert res.status_code == 403

    res = admin_client.delete(f"/users/{test_user['id']}")
    assert res.status_code == 204


def test_selfdelete_admin(admin_client, test_admin):
    res = admin_client.delete(f"/users/{test_admin['id']}")
    assert res.status_code == 403


def test_delete_user_user(authorized_client, test_user):
    res = authorized_client.delete(f"/users/{test_user['id']}")
    assert res.status_code == 403


def test_delete_owner_user(authorized_client, test_owner):
    res = authorized_client.delete(f"/users/{test_owner['id']}")
    assert res.status_code == 403


def test_delete_admin_user(authorized_client, test_admin2):
    res = authorized_client.delete(f"/users/{test_admin2['id']}")
    assert res.status_code == 403


def test_delete_user_unauthorized(client, test_user):
    res = client.delete(f"/users/{test_user['id']}")
    assert res.status_code == 401
