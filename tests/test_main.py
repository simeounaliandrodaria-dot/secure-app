import unittest
import json
from app.main import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health(self):
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"status": "ok"})

    def test_add(self):
        resp = self.client.post("/add", json={"a": 1, "b": 2})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"result": 3.0})

    def test_add_missing(self):
        resp = self.client.post("/add", json={"a": 1})
        self.assertEqual(resp.status_code, 400)

    def test_add_invalid(self):
        resp = self.client.post("/add", json={"a": "bad", "b": 2})
        self.assertEqual(resp.status_code, 400)

if __name__ == "__main__":
    unittest.main()