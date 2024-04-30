from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# ADD ACC ROUTE

def test_add_acc_success():
    acc_data = {
        "id_entity": 1,
        "type": "operation",
        "cost": 97.00
    }

    response = client.post("/add/acc", json=acc_data)

    assert response.status_code == 201

    assert response.text == '"Created"'


def test_add_acc_entity_not_exists():
    acc_data = {
        "id_entity": 999,
        "type": "operation",
        "cost": 100.00
    }

    response = client.post("/add/acc", json=acc_data)

    assert response.status_code == 409

    assert response.json()["detail"] == "Entity not exists in database."


# LIST ACC ROUTE

def test_list_acc_success():
    params = {
        "entity": 1,
    }

    response = client.get("/list/acc/", params=params)

    assert response.status_code == 200

    assert len(response.json()) > 0


def test_list_acc_no_params():
    response = client.get("/list/acc/")

    assert response.status_code == 400

    assert response.json()["detail"] == "At least one parameter should be passed."


def test_list_acc_not_found():
    params = {
        "entity": 999,
        "type": "example",
        "id": 9999
    }

    response = client.get("/list/acc/", params=params)

    assert response.status_code == 404

    assert response.json()["detail"] == "Not found accounts payable with these parameters."
