from fastapi.testclient import TestClient
import main

client = TestClient(main.app)

def setup_function():
    # Make each test independent
    main._reset_state_for_tests()

def test_time_default_ok():
    resp = client.get("/time")
    assert resp.status_code == 200
    t = resp.json()["time"]
    assert "T" in t # ISO-ish clock

def test_time_seconds_trims_microseconds():
    resp = client.get("/time?format=seconds")
    assert resp.status_code == 200
    t = resp.json()["time"]
    assert "." not in t # No microseconds when format=seconds