"""Unit tests for FastAPI endpoints."""
import pytest
from fastapi.testclient import TestClient
from app.main import app
import io


client = TestClient(app)
