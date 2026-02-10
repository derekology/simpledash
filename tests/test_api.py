"""Unit tests for FastAPI endpoints."""
import pytest
from fastapi.testclient import TestClient
from app.main import app
import io


client = TestClient(app)


class TestHealthEndpoint:
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "max_file_size" in data
        assert "max_files" in data


class TestParseEndpoint:
    def test_parse_valid_csv(self):
        csv_content = """Campaign name,Subject,Email title,Status,Sent,Delivered,Opens,Open rate,Clicks,Click rate,Unsubscribes,Unsubscribe rate,Spam complaints,Bounces,Bounce rate
Test Campaign,Test Subject,Test Email,Sent,"2024-01-15 10:00",1000,250,25.0%,50,5.0%,5,0.5%,2,10,1.0%"""
        
        files = [
            ("files", ("test.csv", io.BytesIO(csv_content.encode()), "text/csv"))
        ]
        
        response = client.post("/parse", files=files)
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "errors" in data
        assert len(data["results"]) > 0

    def test_parse_non_csv_file(self):
        files = [
            ("files", ("test.txt", io.BytesIO(b"not a csv"), "text/plain"))
        ]
        
        response = client.post("/parse", files=files)
        assert response.status_code == 200
        data = response.json()
        assert len(data["errors"]) > 0
        assert "Only CSV files supported" in data["errors"][0]["error"]

    def test_parse_too_many_files(self):
        # Create more than MAX_FILES (default 12)
        files = [
            ("files", (f"test{i}.csv", io.BytesIO(b"test"), "text/csv"))
            for i in range(15)
        ]
        
        response = client.post("/parse", files=files)
        assert response.status_code == 400
        assert "Too many files" in response.json()["detail"]

    def test_parse_empty_file(self):
        files = [
            ("files", ("empty.csv", io.BytesIO(b""), "text/csv"))
        ]
        
        response = client.post("/parse", files=files)
        assert response.status_code == 200
        data = response.json()
        assert len(data["errors"]) > 0

    def test_parse_multiple_valid_files(self):
        csv1 = """Campaign Name,Send Date/Time,Emails Sent,Successful Deliveries,Total Opens,Total Clicks,Unsubscribes,Soft Bounces,Hard Bounces,Abuse Reports
Campaign 1,6/9/2018 21:30,1000,990,250,50,5,5,5,2"""
        
        csv2 = """Campaign Name,Send Date/Time,Emails Sent,Successful Deliveries,Total Opens,Total Clicks,Unsubscribes,Soft Bounces,Hard Bounces,Abuse Reports
Campaign 2,6/10/2018 10:00,2000,1980,500,100,10,10,10,4"""
        
        files = [
            ("files", ("test1.csv", io.BytesIO(csv1.encode()), "text/csv")),
            ("files", ("test2.csv", io.BytesIO(csv2.encode()), "text/csv"))
        ]
        
        response = client.post("/parse", files=files)
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) >= 2

    def test_deduplication(self):
        # Upload same campaign twice (same subject, title, date, platform)
        csv_content = """Campaign Name,Send Date/Time,Emails Sent,Successful Deliveries,Total Opens,Total Clicks,Unsubscribes,Soft Bounces,Hard Bounces,Abuse Reports
Test Campaign,6/9/2018 21:30,1000,990,250,50,5,5,5,2"""
        
        files = [
            ("files", ("test1.csv", io.BytesIO(csv_content.encode()), "text/csv")),
            ("files", ("test2.csv", io.BytesIO(csv_content.encode()), "text/csv"))
        ]
        
        response = client.post("/parse", files=files)
        assert response.status_code == 200
        data = response.json()
        # Should deduplicate to 1 campaign
        assert len(data["results"]) == 1


class TestStaticFiles:
    def test_favicon_route(self):
        # Test that favicon route exists (may 404 if not built)
        response = client.get("/favicon.ico")
        # Should return either 200 or 404, not 500
        assert response.status_code in [200, 404]

    def test_spa_fallback(self):
        # Test that SPA fallback works for non-API routes
        response = client.get("/some-random-path")
        # Should return either 200 (if built) or 404 (if not built)
        assert response.status_code in [200, 404]
