import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient
from app.config import settings
from app.database import get_db
from app.models import Base

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}-test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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
    from app.main import app

    def override_get_db():

        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def create_user(client):
    def _create_user(email, password, firstname, surname):
        user_credentials = {
            'firstname': firstname,
            'surname': surname,
            "email": email,
            "password": password,
        }
        res = client.post("/users", json=user_credentials)
        assert res.status_code == 201
        new_user_token = res.json()

        return new_user

    return _create_user


@pytest.fixture
def test_user(create_user):
    return create_user(settings.owner_email, "111", "bebra_t", "some picture of user")


@pytest.fixture
def test_user2(authorized_client, create_user):
    new_user = create_user("bebra_test2@gmail.com", "111", "bebra_t2", "some picture of user2")

    role_data = {
        "name": "Администратор 💫",
        "user_guid": new_user["guid"],
        "color": "aqua"
    }

    res = authorized_client.post("/roles", json=role_data)
    assert res.status_code == 201

    res = authorized_client.get(f"/users/{new_user['guid']}")
    assert res.status_code == 200

    updated_user = res.json()
    updated_user["password"] = new_user["password"]

    return updated_user


@pytest.fixture
def test_user3(create_user):
    return create_user("bebra_test3@gmail.com", "111", "bebra_t3", "some picture of user3")


@pytest.fixture
def get_token(client):
    def _get_token(user):
        res = client.post(
            "/login",
            json={"email": user["email"], "password": user["password"]},
        )
        assert res.status_code == 200
        return res.json()

    return _get_token


@pytest.fixture
def token_owner(get_token, test_user):
    return get_token(test_user)


@pytest.fixture
def token_admin(get_token, test_user2):
    return get_token(test_user2)


@pytest.fixture
def token_common(get_token, test_user3):
    return get_token(test_user3)


@pytest.fixture
def get_authorized_client(client):
    def _get_authorized_client(token):
        new_client = copy(client)
        new_client.headers = {
            **new_client.headers,
            "Authorization": f'Bearer {token["access_token"]}',
        }
        return new_client

    return _get_authorized_client


@pytest.fixture
def authorized_client(get_authorized_client, token_owner):
    return get_authorized_client(token_owner)


@pytest.fixture
def authorized_admin_client(get_authorized_client, token_admin):
    return get_authorized_client(token_admin)


@pytest.fixture
def authorized_common_client(get_authorized_client, token_common):
    return get_authorized_client(token_common)


@pytest.fixture
def test_games(test_user, test_user2, session):
    games_data = [  # Данные для создания игр
        {
            "title": "Тестовая игра",
            "description": "Игра от димы осипенко",
            "img": "some picture",
            "creator_guid": test_user["guid"],
        },
        {
            "title": "Тестовая игра 2",
            "description": "Игра от Николая",
            "img": "some picture 2",
            "creator_guid": test_user["guid"]
        },
        {
            "title": "Тестовая игра 3",
            "description": "Игра от Ильи",
            "img": "some picture 3",
            "creator_guid": test_user2["guid"]
        },
        {
            "title": "Тестовая игра 4",
            "description": "Игра от Поли",
            "img": "some picture 4",
            "creator_guid": test_user2["guid"]
        }

    ]

    def create_game_model(
            game,
    ):
        return models.Game(**game)

    game_map = map(
        create_game_model, games_data
    )
    games_list = list(game_map)

    session.add_all(games_list)
    session.commit()

    games = session.query(models.Game).all()
    return games


@pytest.fixture
def test_updated_data():
    return {"title": "updated title", "description": "updated content", "img": "updated picture"}


@pytest.fixture
def test_roles(test_user, session):
    roles_data = [
        {"name": "test1", "user_guid": test_user["guid"]},
        {"name": "test2", "user_guid": test_user["guid"]},
        {"name": "test3", "user_guid": test_user["guid"]}
    ]

    def create_role_model(
            role,
    ):
        return models.Role(**role)

    role_map = map(
        create_role_model, roles_data
    )
    roles_list = list(role_map)

    session.add_all(roles_list)
    session.commit()

    roles = session.query(models.Role).all()
    return roles


@pytest.fixture
def test_updated_role_data(test_user2):
    return {"name": "new_test", "user_guid": test_user2.guid}