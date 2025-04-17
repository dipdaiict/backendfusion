# import pytest
# from httpx import AsyncClient
# from app.main import app

# @pytest.mark.asyncio
# async def test_health_check():
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.get("/health")
#     assert response.status_code == 200
#     assert response.json() == {"status": "ok"}

from fastapi.testclient import TestClient
from app.main import app  # Import the FastAPI app

client = TestClient(app)  # Create a TestClient instance

def test_health_check():
    response = client.get("/system/health")  # Send a GET request to the /health endpoint
    assert response.status_code == 200  # Check if the status code is 200
    assert response.json() == {"status": "ok"}  # Check if the response body is correct

