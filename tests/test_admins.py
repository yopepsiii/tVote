from app import models


def test_get_admins(admin_client, test_admin2):
    res = admin_client.get('/admins')
    assert res.status_code == 200
    admins = res.json()

    assert models.Admin(**admins[0])


def test_get_admins_owner(owner_client, test_admin2):
    res = owner_client.get('/admins')
    assert res.status_code == 200
    admins = res.json()

    assert models.Admin(**admins[0])


def test_get_admins_user(authorized_client):
    res = authorized_client.get('/admins')
    assert res.status_code == 403


def test_get_admins_unauthorized(client):
    res = client.get('/admins')
    assert res.status_code == 401


def test_create_admin_admin(admin_client, test_user):
    data = {'user_id': test_user['id']}
    res = admin_client.post('/admins', json=data)

    assert res.status_code == 403


def test_create_admin_user(authorized_client, test_user):
    data = {'user_id': test_user['id']}
    res = authorized_client.post('/admins', json=data)

    assert res.status_code == 403


def test_create_admin_unauthorized(client, test_user):
    data = {'user_id': test_user['id']}
    res = client.post('/admins', json=data)

    assert res.status_code == 401


def test_delete_admin(admin_client, test_admin2):
    res = admin_client.delete(f'/admins/{test_admin2["id"]}')
    assert res.status_code == 403


def test_delete_admin_owner(owner_client, test_admin2):
    res = owner_client.delete(f'/admins/{test_admin2['id']}')
    assert res.status_code == 204


def test_delete_admin_user(authorized_client, test_admin2):
    res = authorized_client.delete(f'/admins/{test_admin2["id"]}')
    assert res.status_code == 403


def test_delete_admin_unauthorized(client, test_admin2):
    res = client.delete(f'/admins/{test_admin2["id"]}')
    assert res.status_code == 401
