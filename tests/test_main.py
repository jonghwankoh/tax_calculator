from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "연말정산 계산기" in response.text

def test_calculate_success():
    response = client.post("/calculate", data={"income": 30000000})
    assert response.status_code == 200
    assert "연말정산 결과" in response.text
    assert "30000000" in response.text

def test_calculate_failure():
    response = client.post("/calculate", data={"income": "invalid"})
    assert response.status_code == 422  # Unprocessable Entity
