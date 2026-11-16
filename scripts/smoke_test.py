from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
print("Health:", client.get("/health").json())
print("UI:", client.get("/").status_code)
