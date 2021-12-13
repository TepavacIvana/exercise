from unittest.mock import patch
from freezegun import freeze_time
import pytest
from my_app.routes import app as flask_app


@pytest.fixture
def client():
    client = flask_app.test_client()
    return client


@pytest.fixture
def uuid():
    uuid.return_value = 123
    return uuid


@pytest.fixture()
def expected_note():
    return {"123": {"note": "not possible",
                    "time_created": "Tue, 25 May 2021 14:58:32 GMT",
                    "title": "Neki naslov",
                    "user_id": 7}}


def test_empty_storage(client):
    res = client.get('/api/note')

    assert res.status_code == 200
    assert res.get_json() == {}


@freeze_time("Tue, 25 May 2021 14:58:32 GMT")
def test_create_note(client, uuid):
    with patch.dict('my_app.routes.storage', {}):
        data = {"note": "not possible",
                "title": "Neki naslov",
                "user_id": 7}
        res = client.post('/api/note', json=data)

        assert res.status_code == 200
        assert res.get_json() == {"note": "not possible",
                                  "time_created": "Tue, 25 May 2021 14:58:32 GMT",
                                  "title": "Neki naslov",
                                  "user_id": 7}


def test_create_note_without_title(client):
    data = {
        "note": "not possible",
        "user_id": 7
    }
    res = client.post('/api/note', json=data)

    assert res.status_code == 400
    assert res.json == {'title': ['Missing data for required field.']}


def test_create_note_with_too_long_title(client):
    data = {
        "note": "not possible",
        "title": "Neki komplikovan i dugacak naslov",
        "user_id": 7
    }
    res = client.post('/api/note', json=data)

    assert res.status_code == 400
    assert res.json == {'title': ['Longer than maximum length 20.']}


def test_create_note_with_forbidden_word(client):
    data = {
        "note": "impossible",
        "title": "Neki naslov",
        "user_id": 7
    }
    res = client.post('/api/note', json=data)

    assert res.status_code == 400
    assert res.json == {'note': ['Value should not contain forbidden words']}


def test_create_note_with_negative_user_id(client):
    data = {
        "note": "not possible",
        "title": "Neki naslov",
        "user_id": -1
    }
    res = client.post('/api/note', json=data)

    assert res.status_code == 400
    assert res.get_json() == {'user_id': ['Must be greater than or equal to 1.']}


def test_listing_notes(client, expected_note):
    with patch.dict('my_app.routes.storage', expected_note):
        res = client.get('/api/note')

        assert res.status_code == 200
        assert res.get_json() == {"123": {"note": "not possible",
                                          "time_created": "Tue, 25 May 2021 14:58:32 GMT",
                                          "title": "Neki naslov",
                                          "user_id": 7}}


def test_retrieving_a_single_note(client, expected_note):
    with patch.dict('my_app.routes.storage', expected_note):
        res = client.get('/api/note/123')

        assert res.status_code == 200
        assert res.get_json() == {"note": "not possible",
                                  "time_created": "Tue, 25 May 2021 14:58:32 GMT",
                                  "title": "Neki naslov",
                                  "user_id": 7}


def test_retrieving_a_note_that_does_not_exist(client):
    res = client.get('/api/note/12345')

    assert res.status_code == 404
    assert res.get_json() == {'message': 'Not found'}


@freeze_time("Tue, 25 May 2021 16:00:00 GMT")
def test_updating_a_note(client, expected_note):
    with patch.dict('my_app.routes.storage', expected_note):
        data = {"title": "Cetvrtak"}
        res = client.patch('/api/note/123', json=data)

        assert res.status_code == 200
        assert res.get_json() == {"note": "not possible",
                                  "time_created": "Tue, 25 May 2021 14:58:32 GMT",
                                  "time_updated": "Tue, 25 May 2021 16:00:00 GMT",
                                  "title": "Cetvrtak",
                                  "user_id": 7}


def test_updating_a_note_with_too_long_title(client, expected_note):
    with patch.dict('my_app.routes.storage', expected_note):
        data = {"title": "Ja sam dugacak i krsim pravilo"}
        res = client.patch('/api/note/123', json=data)

        assert res.status_code == 400
        assert res.get_json() == {'title': ['Longer than maximum length 20.']}


def test_updating_a_note_with_forbidden_word(client, expected_note):
    with patch.dict('my_app.routes.storage', expected_note):
        data = {"note": "impossible"}
        res = client.patch('/api/note/123', json=data)

        assert res.status_code == 400
        assert res.get_json() == {'note': ['Value should not contain forbidden words']}


def test_updating_a_note_that_does_not_exist(client):
    data = {"title": "Cetvrtak"}
    res = client.patch('/api/note/12345', json=data)

    assert res.status_code == 404
    assert res.get_json() == {'message': 'Not found'}


def test_deleting_a_note(client, expected_note):
    with patch.dict('my_app.routes.storage', expected_note):
        res = client.delete('/api/note/123')

        assert res.status_code == 200
        assert res.get_json() == {'message': 'Note has been deleted'}


def test_deleting_a_note_that_does_not_exist(client):
    res = client.delete('/api/note/12345')

    assert res.status_code == 404
    assert res.get_json() == {'message': 'Not found'}


