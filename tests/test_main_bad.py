import unittest
import json
from app.main_bad import app

class TestAppBad(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health(self):
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"status": "ok"})

    def test_add(self):
        # This passes
        resp = self.client.post("/add", json={"a": 1, "b": 2})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"result": 3})

    def test_add_string_concat(self):
        # This will fail, triggers bug (should reject string input, but does not)
        resp = self.client.post("/add", json={"a": "1", "b": "2"})
        self.assertEqual(resp.status_code, 400)

if __name__ == "__main__":
    unittest.main()