def test_health_exposes_selected_providers(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "service": "DIGITAL TECHNICAL",
        "status": "ok",
        "environment": "test",
        "ai_provider": "deterministic",
        "cloud_provider": "local",
    }


def test_submit_and_read_request(client):
    created = client.post(
        "/v1/requests",
        json={
            "question": "How should a cloud architecture change be validated?",
            "criticality": "medium",
            "requester": "platform-team",
        },
    )
    assert created.status_code == 201
    assert created.json()["status"] == "completed"
    assert created.json()["sources"]

    fetched = client.get(f"/v1/requests/{created.json()['request_id']}")
    assert fetched.status_code == 200
    assert fetched.json() == created.json()


def test_critical_request_requires_review(client):
    response = client.post(
        "/v1/requests",
        json={"question": "Production database is unavailable", "criticality": "critical"},
    )
    assert response.status_code == 201
    assert response.json()["status"] == "human_review"


def test_missing_source_requires_review(client):
    response = client.post(
        "/v1/requests",
        json={"question": "Explain an unrelated invented component", "criticality": "low"},
    )
    assert response.status_code == 201
    assert response.json()["status"] == "human_review"


def test_validation_and_not_found(client):
    assert client.post("/v1/requests", json={"question": "no"}).status_code == 422
    assert client.get("/v1/requests/missing").status_code == 404
