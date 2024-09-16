from copy import copy

import pytest
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from app import models, utils
from app.main import app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient
from starlette.datastructures import FormData

from config import settings
from app.database import get_db
from app.models import Base

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}-test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True, scope="function")
def fastapi_cache():
    FastAPICache.init(InMemoryBackend())


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def create_user(owner_client):
    def _create_user(email, password, firstname, surname):
        user_credentials = {
            'firstname': firstname,
            'surname': surname,
            "email": email,
            "password": password,
        }
        res = owner_client.post("/users", json=user_credentials)
        assert res.status_code == 201
        new_user = res.json()

        new_user['password'] = password

        assert new_user['firstname'] == firstname
        assert new_user['surname'] == surname
        assert new_user['email'] == email
        assert new_user['password'] == password

        return new_user

    return _create_user


@pytest.fixture
def test_user(create_user):
    return create_user('test_user@test.com', "test", "test", "test")


@pytest.fixture
def test_admin(owner_client, create_user):
    new_user = create_user("test_admin@test.com", "test", "test_admin", "test_admin")

    res = owner_client.post("/admins", json={'user_id': new_user['id']})
    assert res.status_code == 201

    new_admin = res.json()
    new_admin['password'] = 'test'
    return new_admin


@pytest.fixture
def test_admin2(owner_client, create_user):
    new_user = create_user("test_admin2@test.com", "test2", "test_admin2", "test_admin2")

    res = owner_client.post("/admins", json={'user_id': new_user['id']})
    assert res.status_code == 201

    new_admin = res.json()
    new_admin['password'] = 'test2'
    return new_admin


@pytest.fixture
def test_owner(session):
    user = models.User(firstname='test', surname='test', email=settings.owner_email, password=utils.hash('test'))
    session.add(user)
    session.commit()
    session.refresh(user)

    user_model = models.User(id=user.id, firstname=user.firstname, surname=user.surname, email=user.email,
                             password='test', created_at=user.created_at)

    return user_model.__dict__


@pytest.fixture
def get_token(client):
    def _get_token(user):
        formData = FormData(username=user['email'], password=user['password'])
        res = client.post(
            "/login",
            data=formData,
        )
        assert res.status_code == 200
        return res.json()

    return _get_token


@pytest.fixture
def get_authorized_client(client):
    def _get_authorized_client(token):
        new_client = copy(client)
        new_client.headers = {
            **new_client.headers,
            "Authorization": f'Bearer {token['access_token']}',
        }
        return new_client

    return _get_authorized_client


@pytest.fixture
def owner_client(get_authorized_client, token_owner):
    return get_authorized_client(token_owner)


@pytest.fixture
def admin_client(get_authorized_client, token_admin):
    return get_authorized_client(token_admin)


@pytest.fixture
def admin_client2(get_authorized_client, token_admin2):
    return get_authorized_client(token_admin2)


@pytest.fixture
def authorized_client(get_authorized_client, token_user):
    return get_authorized_client(token_user)


@pytest.fixture
def token_owner(get_token, test_owner):
    return get_token(test_owner)


@pytest.fixture
def token_admin(get_token, test_admin):
    return get_token(test_admin)


@pytest.fixture
def token_admin2(get_token, test_admin2):
    return get_token(test_admin2)


@pytest.fixture
def token_user(get_token, test_user):
    return get_token(test_user)


@pytest.fixture
def test_candidate(admin_client):
    data = {'firstname': 'test_candidate_firstname',
            'surname': 'test_candidate_surname',
            'year_of_study': 2,
            'group': 'test_candidate_group',
            'study_dirrection': 'test_candidate_study_dirrection',
            'photo': 'test_candidate_photo'}
    res = admin_client.post('/candidates', json=data)
    assert res.status_code == 201
    new_candidate = res.json()

    assert new_candidate['firstname'] == 'test_candidate_firstname'
    assert new_candidate['surname'] == 'test_candidate_surname'
    assert new_candidate['year_of_study'] == 2
    assert new_candidate['group'] == 'test_candidate_group'
    assert new_candidate['study_dirrection'] == 'test_candidate_study_dirrection'
    assert new_candidate['photo'] == 'test_candidate_photo'

    return new_candidate


@pytest.fixture
def test_candidate2(admin_client):
    data = {'firstname': 'test_candidate2_firstname',
            'surname': 'test_candidate2_surname',
            'year_of_study': 3,
            'group': 'test_candidate2_group',
            'study_dirrection': 'test_candidate2_study_dirrection',
            'photo': 'test_candidate2_photo'}
    res = admin_client.post('/candidates', json=data)
    assert res.status_code == 201
    new_candidate = res.json()

    assert new_candidate['firstname'] == data['firstname']
    assert new_candidate['surname'] == data['surname']
    assert new_candidate['year_of_study'] == data['year_of_study']
    assert new_candidate['group'] == data['group']
    assert new_candidate['study_dirrection'] == data['study_dirrection']
    assert new_candidate['photo'] == data['photo']

    return new_candidate
