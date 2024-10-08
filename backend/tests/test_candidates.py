import pytest

from backend.app import models

parametrs = [
    (
        "test-name",
        "test-surname",
        1,
        "test-group",
        "test-study-dirrection",
        "test-photo",
        201,
    ),
    (
        1,
        "test-surname",
        "TEXT",
        "test-group",
        "test-study-dirrection",
        "test-photo",
        422,
    ),
    (None, "test-surname", 1, "test-group", "test-study-dirrection", "test-photo", 422),
    (None, None, 1, "test-group", "test-study-dirrection", "test-photo", 422),
    (None, None, None, "test-group", "test-study-dirrection", "test-photo", 422),
    (None, None, None, None, "test-study-dirrection", "test-photo", 422),
    (None, None, None, None, "test-study-dirrection", "test-photo", 422),
    (None, None, None, None, None, "test-photo", 422),
    (None, None, None, None, None, None, 422),
]


def test_get_candidates(admin_client, fastapi_cache):
    data = {
        "firstname": "test",
        "surname": "test",
        "year_of_study": 1,
        "group": "test",
        "study_dirrection": "test",
        "photo": "test",
    }
    first_res = admin_client.post("/candidates", json=data)

    res = admin_client.get("/candidates")
    assert res.status_code == 200

    candidates = res.json()
    assert models.Candidate(**candidates[0])


@pytest.mark.parametrize(
    "firstname, surname, year_of_study, group, study_dirrection, photo, status",
    [
        (
            "test-name",
            "test-surname",
            1,
            "test-group",
            "test-study-dirrection",
            "test-photo",
            201,
        ),
        (
            1,
            "test-surname",
            "TEXT",
            "test-group",
            "test-study-dirrection",
            "test-photo",
            422,
        ),
        (
            None,
            "test-surname",
            1,
            "test-group",
            "test-study-dirrection",
            "test-photo",
            422,
        ),
        (None, None, 1, "test-group", "test-study-dirrection", "test-photo", 422),
        (None, None, None, "test-group", "test-study-dirrection", "test-photo", 422),
        (None, None, None, None, "test-study-dirrection", "test-photo", 422),
        (None, None, None, None, "test-study-dirrection", "test-photo", 422),
        (None, None, None, None, None, "test-photo", 422),
        (None, None, None, None, None, None, 422),
    ],
)
def test_create_candidate(
    admin_client,
    fastapi_cache,
    firstname,
    surname,
    year_of_study,
    group,
    study_dirrection,
    photo,
    status,
):
    data = {
        "firstname": firstname,
        "surname": surname,
        "year_of_study": year_of_study,
        "group": group,
        "study_dirrection": study_dirrection,
        "photo": photo,
    }
    res = admin_client.post("/candidates", json=data)
    assert res.status_code == status
    if res.status_code == 201:
        assert models.Candidate(**res.json())


@pytest.mark.parametrize(
    "firstname, surname, year_of_study, group, study_dirrection, photo, status",
    [
        (
            "test-name",
            "test-surname",
            1,
            "test-group",
            "test-study-dirrection",
            "test-photo",
            201,
        ),
        (
            1,
            "test-surname",
            "TEXT",
            "test-group",
            "test-study-dirrection",
            "test-photo",
            422,
        ),
        (
            None,
            "test-surname",
            1,
            "test-group",
            "test-study-dirrection",
            "test-photo",
            422,
        ),
        (None, None, 1, "test-group", "test-study-dirrection", "test-photo", 422),
        (None, None, None, "test-group", "test-study-dirrection", "test-photo", 422),
        (None, None, None, None, "test-study-dirrection", "test-photo", 422),
        (None, None, None, None, "test-study-dirrection", "test-photo", 422),
        (None, None, None, None, None, "test-photo", 422),
        (None, None, None, None, None, None, 422),
    ],
)
def test_create_candidate_owner(
    owner_client,
    fastapi_cache,
    firstname,
    surname,
    year_of_study,
    group,
    study_dirrection,
    photo,
    status,
):
    data = {
        "firstname": firstname,
        "surname": surname,
        "year_of_study": year_of_study,
        "group": group,
        "study_dirrection": study_dirrection,
        "photo": photo,
    }
    res = owner_client.post("/candidates", json=data)
    assert res.status_code == status
    if res.status_code == 201:
        assert models.Candidate(**res.json())


@pytest.mark.parametrize(
    "firstname, surname, year_of_study, group, study_dirrection, photo",
    [
        (
            "test-name",
            "test-surname",
            1,
            "test-group",
            "test-study-dirrection",
            "test-photo",
        ),
        (
            1,
            "test-surname",
            "TEXT",
            "test-group",
            "test-study-dirrection",
            "test-photo",
        ),
        (None, "test-surname", 1, "test-group", "test-study-dirrection", "test-photo"),
        (None, None, 1, "test-group", "test-study-dirrection", "test-photo"),
        (None, None, None, "test-group", "test-study-dirrection", "test-photo"),
        (None, None, None, None, "test-study-dirrection", "test-photo"),
        (None, None, None, None, "test-study-dirrection", "test-photo"),
        (None, None, None, None, None, "test-photo"),
        (None, None, None, None, None, None),
    ],
)
def test_create_candidate_user(
    authorized_client,
    fastapi_cache,
    firstname,
    surname,
    year_of_study,
    group,
    study_dirrection,
    photo,
):
    data = {
        "firstname": firstname,
        "surname": surname,
        "year_of_study": year_of_study,
        "group": group,
        "study_dirrection": study_dirrection,
        "photo": photo,
    }
    res = authorized_client.post("/candidates", json=data)
    assert res.status_code == 403


@pytest.mark.parametrize(
    "firstname, surname, year_of_study, group, study_dirrection, photo",
    [
        (
            "test-name",
            "test-surname",
            1,
            "test-group",
            "test-study-dirrection",
            "test-photo",
        ),
        (
            1,
            "test-surname",
            "TEXT",
            "test-group",
            "test-study-dirrection",
            "test-photo",
        ),
        (None, "test-surname", 1, "test-group", "test-study-dirrection", "test-photo"),
        (None, None, 1, "test-group", "test-study-dirrection", "test-photo"),
        (None, None, None, "test-group", "test-study-dirrection", "test-photo"),
        (None, None, None, None, "test-study-dirrection", "test-photo"),
        (None, None, None, None, "test-study-dirrection", "test-photo"),
        (None, None, None, None, None, "test-photo"),
        (None, None, None, None, None, None),
    ],
)
def test_create_candidate_unauthorized(
    client,
    fastapi_cache,
    firstname,
    surname,
    year_of_study,
    group,
    study_dirrection,
    photo,
):
    data = {
        "firstname": firstname,
        "surname": surname,
        "year_of_study": year_of_study,
        "group": group,
        "study_dirrection": study_dirrection,
        "photo": photo,
    }
    res = client.post("/candidates", json=data)
    assert res.status_code == 401


@pytest.mark.parametrize(
    "firstname, surname, year_of_study, group, study_dirrection, photo",
    [
        (
            "test-name",
            "test-surname",
            1,
            "test-group",
            "test-study-dirrection",
            "test-photo",
        ),
        (None, "test-surname", 1, "test-group", "test-study-dirrection", "test-photo"),
        (None, None, 1, "test-group", "test-study-dirrection", "test-photo"),
        (None, None, None, "test-group", "test-study-dirrection", "test-photo"),
        (None, None, None, None, "test-study-dirrection", "test-photo"),
        (None, None, None, None, "test-study-dirrection", "test-photo"),
        (None, None, None, None, None, "test-photo"),
        (None, None, None, None, None, None),
    ],
)
def test_update_candidate(
    admin_client,
    test_candidate,
    fastapi_cache,
    firstname,
    surname,
    year_of_study,
    group,
    study_dirrection,
    photo,
):
    data = {
        "firstname": firstname,
        "surname": surname,
        "year_of_study": year_of_study,
        "group": group,
        "study_dirrection": study_dirrection,
        "photo": photo,
    }
    update_data = {k: v for k, v in data.items() if v is not None}
    res = admin_client.patch(f"/candidates/{test_candidate['id']}", json=update_data)
    assert res.status_code == 200

    updated_candidate = res.json()

    if firstname:
        assert updated_candidate["firstname"] == firstname
    if surname:
        assert updated_candidate["surname"] == surname
    if year_of_study:
        assert updated_candidate["year_of_study"] == year_of_study
    if group:
        assert updated_candidate["group"] == group
    if study_dirrection:
        assert updated_candidate["study_dirrection"] == study_dirrection
    if photo:
        assert updated_candidate["photo"] == photo


@pytest.mark.parametrize(
    "firstname, surname, year_of_study, group, study_dirrection, photo",
    [
        (
            "test-name",
            "test-surname",
            1,
            "test-group",
            "test-study-dirrection",
            "test-photo",
        ),
        (None, "test-surname", 1, "test-group", "test-study-dirrection", "test-photo"),
        (None, None, 1, "test-group", "test-study-dirrection", "test-photo"),
        (None, None, None, "test-group", "test-study-dirrection", "test-photo"),
        (None, None, None, None, "test-study-dirrection", "test-photo"),
        (None, None, None, None, "test-study-dirrection", "test-photo"),
        (None, None, None, None, None, "test-photo"),
        (None, None, None, None, None, None),
    ],
)
def test_update_candidate_owner(
    owner_client,
    test_candidate,
    fastapi_cache,
    firstname,
    surname,
    year_of_study,
    group,
    study_dirrection,
    photo,
):
    data = {
        "firstname": firstname,
        "surname": surname,
        "year_of_study": year_of_study,
        "group": group,
        "study_dirrection": study_dirrection,
        "photo": photo,
    }
    update_data = {k: v for k, v in data.items() if v is not None}
    res = owner_client.patch(f"/candidates/{test_candidate['id']}", json=update_data)
    assert res.status_code == 200

    updated_candidate = res.json()

    if firstname:
        assert updated_candidate["firstname"] == firstname
    if surname:
        assert updated_candidate["surname"] == surname
    if year_of_study:
        assert updated_candidate["year_of_study"] == year_of_study
    if group:
        assert updated_candidate["group"] == group
    if study_dirrection:
        assert updated_candidate["study_dirrection"] == study_dirrection
    if photo:
        assert updated_candidate["photo"] == photo


@pytest.mark.parametrize(
    "firstname, surname, year_of_study, group, study_dirrection, photo",
    [
        (
            "test-name",
            "test-surname",
            1,
            "test-group",
            "test-study-dirrection",
            "test-photo",
        ),
        (None, "test-surname", 1, "test-group", "test-study-dirrection", "test-photo"),
        (None, None, 1, "test-group", "test-study-dirrection", "test-photo"),
        (None, None, None, "test-group", "test-study-dirrection", "test-photo"),
        (None, None, None, None, "test-study-dirrection", "test-photo"),
        (None, None, None, None, "test-study-dirrection", "test-photo"),
        (None, None, None, None, None, "test-photo"),
        (None, None, None, None, None, None),
    ],
)
def test_update_candidate_user(
    authorized_client,
    test_candidate,
    fastapi_cache,
    firstname,
    surname,
    year_of_study,
    group,
    study_dirrection,
    photo,
):
    data = {
        "firstname": firstname,
        "surname": surname,
        "year_of_study": year_of_study,
        "group": group,
        "study_dirrection": study_dirrection,
        "photo": photo,
    }
    update_data = {k: v for k, v in data.items() if v is not None}
    res = authorized_client.patch(
        f"/candidates/{test_candidate['id']}", json=update_data
    )
    assert res.status_code == 403


@pytest.mark.parametrize(
    "firstname, surname, year_of_study, group, study_dirrection, photo",
    [
        (
            "test-name",
            "test-surname",
            1,
            "test-group",
            "test-study-dirrection",
            "test-photo",
        ),
        (
            1,
            "test-surname",
            "TEXT",
            "test-group",
            "test-study-dirrection",
            "test-photo",
        ),
        (None, "test-surname", 1, "test-group", "test-study-dirrection", "test-photo"),
        (None, None, 1, "test-group", "test-study-dirrection", "test-photo"),
        (None, None, None, "test-group", "test-study-dirrection", "test-photo"),
        (None, None, None, None, "test-study-dirrection", "test-photo"),
        (None, None, None, None, "test-study-dirrection", "test-photo"),
        (None, None, None, None, None, "test-photo"),
        (None, None, None, None, None, None),
    ],
)
def test_update_candidate_unauthorized(
    client,
    test_candidate,
    fastapi_cache,
    firstname,
    surname,
    year_of_study,
    group,
    study_dirrection,
    photo,
):
    data = {
        "firstname": firstname,
        "surname": surname,
        "year_of_study": year_of_study,
        "group": group,
        "study_dirrection": study_dirrection,
        "photo": photo,
    }
    update_data = {k: v for k, v in data.items() if v is not None}
    res = client.patch(f"/candidates/{test_candidate['id']}", json=update_data)
    assert res.status_code == 401


def test_update_candidate_wrong_id(admin_client, fastapi_cache):
    data = {
        "firstname": "test-name",
        "surname": "test-surname",
        "year_of_study": 1,
        "group": "test-group",
        "study_dirrection": "test-study-dirrection",
        "photo": "test-photo",
    }
    res = admin_client.patch("/candidates/999999999", json=data)
    assert res.status_code == 404


def test_delete_candidate(admin_client, test_candidate, fastapi_cache):
    res = admin_client.delete(f'/candidates/{test_candidate["id"]}')
    assert res.status_code == 204


def test_delete_candidate_owner(owner_client, test_candidate, fastapi_cache):
    res = owner_client.delete(f'/candidates/{test_candidate["id"]}')
    assert res.status_code == 204


def test_delete_candidate_user(authorized_client, test_candidate, fastapi_cache):
    res = authorized_client.delete(f'/candidates/{test_candidate["id"]}')
    assert res.status_code == 403


def test_delete_candidate_wrong_id(admin_client, fastapi_cache):
    res = admin_client.delete(f"/candidates/9999999999999999")
    assert res.status_code == 404


def test_delete_candidate_unauthorized(client, test_candidate):
    res = client.delete(f"/candidates/{test_candidate['id']}")
    assert res.status_code == 401
