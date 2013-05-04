import unittest
import everest
import json

class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        self.app = everest.app.test_client()

    def tearDown(self):
        pass

    def test_route(self):
        expected = ''.join(json.dumps({ 'source': 60003469, 'destination': 60003469 }).split())
        response = self.app.get('/route/%d/%d/' % (60003469, 60003469))
        result = ''.join(response.data.split())
        assert result == expected

if __name__ == '__main__':
    unittest.main()
