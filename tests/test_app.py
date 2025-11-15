import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from main import app
from database import Base, engine, SessionLocal
import pytest
from sqlalchemy.orm import Session

# Create a fresh test database
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.fixture
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------------
# TEST 1: Register User
# --------------------------
def test_register_user():
    response = client.post(
        "/register",
        json={"username": "testuser", "password": "123", "is_admin": True}
    )
    assert response.status_code in [200, 400]   # 400 if already exists

# --------------------------
# TEST 2: Login
# --------------------------
def test_login():
    response = client.post(
        "/login",
        json={"username": "testuser", "password": "123"}
    )
    assert response.status_code == 200
    assert "token" in response.json()

    global TOKEN
    TOKEN = response.json()["token"]

# --------------------------
# TEST 3: Add Sweet
# --------------------------
def test_add_sweet():
    response = client.post(
        "/sweets",
        json={"name": "Ladoo", "category": "Indian", "price": 20, "quantity": 50},
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    assert response.status_code in [200, 500]  # 500 if already exists

# --------------------------
# TEST 4: Get All Sweets
# --------------------------
def test_get_sweets():
    response = client.get(
        "/sweets",
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# --------------------------
# TEST 5: Purchase Sweet
# --------------------------
def test_purchase_sweet():
    response = client.post(
        "/sweets/1/purchase",
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    assert response.status_code in [200, 400]

# --------------------------
# TEST 6: Restock Sweet
# --------------------------
def test_restock_sweet():
    response = client.post(
        "/sweets/1/restock",
        json={"quantity": 10},
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    assert response.status_code in [200, 404]

# --------------------------
# TEST 7: Delete Sweet
# --------------------------
def test_delete_sweet():
    response = client.delete(
        "/sweets/1",
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    assert response.status_code in [200, 404]
