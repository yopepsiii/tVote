import pytest


def test_vote(authorized_client, test_candidate, fastapi_cache):
    vote_data_1 = {"candidate_id": test_candidate["id"], "type": 1}
    vote_data_2 = {"candidate_id": test_candidate["id"], "type": 1}  # голос удален
    vote_data_3 = {"candidate_id": test_candidate["id"], "type": 0}
    vote_data_4 = {"candidate_id": test_candidate["id"], "type": 0}  # голос удален
    vote_data_5 = {"candidate_id": test_candidate["id"], "type": 1}
    vote_data_6 = {"candidate_id": test_candidate["id"], "type": 0}  # поставлен дизлайк
    vote_data_7 = {"candidate_id": test_candidate["id"], "type": 1}  # поставлен лайк

    res_1 = authorized_client.post("/votes", json=vote_data_1)
    assert res_1.status_code == 200

    vote = res_1.json()
    assert vote["candidate_id"] == test_candidate["id"]
    assert vote["type"] == 1

    res_2 = authorized_client.post("/votes", json=vote_data_2)
    assert res_2.status_code == 200

    vote = res_2.json()
    assert vote["message"] == "Оценка удалена"

    res_3 = authorized_client.post("/votes", json=vote_data_3)
    assert res_3.status_code == 200

    vote = res_3.json()
    assert vote["candidate_id"] == test_candidate["id"]
    assert vote["type"] == 0

    res_4 = authorized_client.post("/votes", json=vote_data_4)
    assert res_4.status_code == 200
    vote = res_4.json()
    assert vote["message"] == "Оценка удалена"

    res_5 = authorized_client.post("/votes", json=vote_data_5)
    assert res_1.status_code == 200

    vote = res_5.json()
    assert vote["candidate_id"] == test_candidate["id"]
    assert vote["type"] == 1

    res_6 = authorized_client.post("/votes", json=vote_data_6)
    assert res_6.status_code == 200
    vote = res_6.json()
    assert vote["type"] == 0
    assert vote["candidate_id"] == test_candidate["id"]

    res_7 = authorized_client.post("/votes", json=vote_data_7)
    assert res_7.status_code == 200

    vote = res_7.json()
    assert vote["type"] == 1
    assert vote["candidate_id"] == test_candidate["id"]


def test_vote_admin(admin_client, test_candidate, fastapi_cache):
    vote_data_1 = {"candidate_id": test_candidate["id"], "type": 1}
    vote_data_2 = {"candidate_id": test_candidate["id"], "type": 1}  # голос удален
    vote_data_3 = {"candidate_id": test_candidate["id"], "type": 0}
    vote_data_4 = {"candidate_id": test_candidate["id"], "type": 0}  # голос удален
    vote_data_5 = {"candidate_id": test_candidate["id"], "type": 1}
    vote_data_6 = {"candidate_id": test_candidate["id"], "type": 0}  # поставлен дизлайк
    vote_data_7 = {"candidate_id": test_candidate["id"], "type": 1}  # поставлен лайк

    res_1 = admin_client.post("/votes", json=vote_data_1)
    assert res_1.status_code == 200

    vote = res_1.json()
    assert vote["candidate_id"] == test_candidate["id"]
    assert vote["type"] == 1

    res_2 = admin_client.post("/votes", json=vote_data_2)
    assert res_2.status_code == 200

    vote = res_2.json()
    assert vote["message"] == "Оценка удалена"

    res_3 = admin_client.post("/votes", json=vote_data_3)
    assert res_3.status_code == 200

    vote = res_3.json()
    assert vote["candidate_id"] == test_candidate["id"]
    assert vote["type"] == 0

    res_4 = admin_client.post("/votes", json=vote_data_4)
    assert res_4.status_code == 200
    vote = res_4.json()
    assert vote["message"] == "Оценка удалена"

    res_5 = admin_client.post("/votes", json=vote_data_5)
    assert res_1.status_code == 200

    vote = res_5.json()
    assert vote["candidate_id"] == test_candidate["id"]
    assert vote["type"] == 1

    res_6 = admin_client.post("/votes", json=vote_data_6)
    assert res_6.status_code == 200
    vote = res_6.json()
    assert vote["type"] == 0
    assert vote["candidate_id"] == test_candidate["id"]

    res_7 = admin_client.post("/votes", json=vote_data_7)
    assert res_7.status_code == 200

    vote = res_7.json()
    assert vote["type"] == 1
    assert vote["candidate_id"] == test_candidate["id"]


def test_vote_owner(owner_client, test_candidate, fastapi_cache):
    vote_data_1 = {"candidate_id": test_candidate["id"], "type": 1}
    vote_data_2 = {"candidate_id": test_candidate["id"], "type": 1}  # голос удален
    vote_data_3 = {"candidate_id": test_candidate["id"], "type": 0}
    vote_data_4 = {"candidate_id": test_candidate["id"], "type": 0}  # голос удален
    vote_data_5 = {"candidate_id": test_candidate["id"], "type": 1}
    vote_data_6 = {"candidate_id": test_candidate["id"], "type": 0}  # поставлен дизлайк
    vote_data_7 = {"candidate_id": test_candidate["id"], "type": 1}  # поставлен лайк

    res_1 = owner_client.post("/votes", json=vote_data_1)
    assert res_1.status_code == 200

    vote = res_1.json()
    assert vote["candidate_id"] == test_candidate["id"]
    assert vote["type"] == 1

    res_2 = owner_client.post("/votes", json=vote_data_2)
    assert res_2.status_code == 200

    vote = res_2.json()
    assert vote["message"] == "Оценка удалена"

    res_3 = owner_client.post("/votes", json=vote_data_3)
    assert res_3.status_code == 200

    vote = res_3.json()
    assert vote["candidate_id"] == test_candidate["id"]
    assert vote["type"] == 0

    res_4 = owner_client.post("/votes", json=vote_data_4)
    assert res_4.status_code == 200
    vote = res_4.json()
    assert vote["message"] == "Оценка удалена"

    res_5 = owner_client.post("/votes", json=vote_data_5)
    assert res_1.status_code == 200

    vote = res_5.json()
    assert vote["candidate_id"] == test_candidate["id"]
    assert vote["type"] == 1

    res_6 = owner_client.post("/votes", json=vote_data_6)
    assert res_6.status_code == 200
    vote = res_6.json()
    assert vote["type"] == 0
    assert vote["candidate_id"] == test_candidate["id"]

    res_7 = owner_client.post("/votes", json=vote_data_7)
    assert res_7.status_code == 200

    vote = res_7.json()
    assert vote["type"] == 1
    assert vote["candidate_id"] == test_candidate["id"]


"""
Наверное, при просмотре этих тестов возник вопрос: почему не через paramirize?
Дело в том, что как я знаю при parametrize полностью создается отдельная функция не зависящая от других

НО, так не проверить логику проставления оценок, поэтому пришлось все в одной функции оставить, чтобы сохранялись
результаты выполнения предыдущих запросов
"""


def test_vote_unauthorized(client, test_candidate, fastapi_cache):
    vote_data_1 = {"candidate_id": test_candidate["id"], "type": 1}
    res_1 = client.post("/votes", json=vote_data_1)
    assert res_1.status_code == 401


def test_vote_wrong_candidate_id(authorized_client, fastapi_cache):
    vote_data_1 = {"candidate_id": 999999999, "type": 1}
    res_1 = authorized_client.post("/votes", json=vote_data_1)
    assert res_1.status_code == 404


def test_new_like_vote(
    authorized_client, test_candidate, test_candidate2, fastapi_cache
):
    vote_data_1 = {"candidate_id": test_candidate["id"], "type": 1}
    res_1 = authorized_client.post("/votes", json=vote_data_1)

    assert res_1.status_code == 200

    vote_data_2 = {"candidate_id": test_candidate2["id"], "type": 1}
    res_2 = authorized_client.post("/votes", json=vote_data_2)

    assert res_2.status_code == 200

    res_3 = authorized_client.get("/candidates")
    assert res_3.status_code == 200

    candidates = res_3.json()

    assert len(candidates) == 2
    assert candidates[0]["likes_count"] == 0
    assert candidates[1]["likes_count"] == 1
