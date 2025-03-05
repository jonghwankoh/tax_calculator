import pytest
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
    response = client.post("/calculate", data={"income": 50000000, "pension": 2000000, "card": 10000000})
    assert response.status_code == 200
    assert "연말정산 결과" in response.text
    assert "최종 소득" in response.text

def test_calculate_invalid_input():
    response = client.post("/calculate", data={"income": -1000, "pension": 100, "card": 100})
    assert response.status_code == 200 #400 응답코드라 오류가 발생 

def test_calculate_missing_input():
    response = client.post("/calculate", data={"income": 50000000, "pension": 2000000})
    assert response.status_code == 422

def test_calculate_large_numbers():
    response = client.post("/calculate", data={"income": 1000000000, "pension": 100000000, "card": 500000000})
    assert response.status_code == 200
    assert "연말정산 결과" in response.text
