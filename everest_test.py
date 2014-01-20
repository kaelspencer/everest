import unittest
import everest
from flask import json

class RouteTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.app = everest.app.test_client()

        expected = ''.join(json.dumps({
              "count": 15,
              "route": [
                {"id": 30000142, "name": "Jita"},
                {"id": 30000144, "name": "Perimeter"},
                {"id": 30002642, "name": "Iyen-Oursta"},
                {"id": 30002643, "name": "Faurent"},
                {"id": 30002644, "name": "Ambeke"},
                {"id": 30002691, "name": "Crielere"},
                {"id": 30002718, "name": "Rancer"},
                {"id": 30002719, "name": "Miroitem"},
                {"id": 30002723, "name": "Otou"},
                {"id": 30002053, "name": "Hek"},
                {"id": 30002543, "name": "Eystur"},
                {"id": 30002544, "name": "Pator"},
                {"id": 30002568, "name": "Onga"},
                {"id": 30002529, "name": "Gyng"},
                {"id": 30002526, "name": "Frarn"},
                {"id": 30002510, "name": "Rens"}
              ]
            }).split())
        self.data = [{
                'url': '/route/%d/%d/' % (30000142, 30002510),
                'expected': expected
            }, {
                'url': '/route/%s/%s/' % ('Jita', 'Rens'),
                'expected': expected
            }, {
                'url': '/route/%s/%d/' % ('Jita', 30002510),
                'expected': expected
            }, {
                'url': '/route/%d/%s/' % (30000142, 'Rens'),
                'expected': expected
            }]

    def runTest(self):
        for test in self.data:
            response = self.app.get(test['url'])
            result = ''.join(response.data.split())
            self.assertEquals(test['expected'], result, test['url'])

class RouteStationTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.app = everest.app.test_client()

        expected = ''.join(json.dumps({
              "count": 15,
              "route": [
                {"id": 30000142, "name": "Jita"},
                {"id": 30000144, "name": "Perimeter"},
                {"id": 30002642, "name": "Iyen-Oursta"},
                {"id": 30002643, "name": "Faurent"},
                {"id": 30002644, "name": "Ambeke"},
                {"id": 30002691, "name": "Crielere"},
                {"id": 30002718, "name": "Rancer"},
                {"id": 30002719, "name": "Miroitem"},
                {"id": 30002723, "name": "Otou"},
                {"id": 30002053, "name": "Hek"},
                {"id": 30002543, "name": "Eystur"},
                {"id": 30002544, "name": "Pator"},
                {"id": 30002568, "name": "Onga"},
                {"id": 30002529, "name": "Gyng"},
                {"id": 30002526, "name": "Frarn"},
                {"id": 30002510, "name": "Rens"}
              ]
            }).split())
        self.data = [{
                'url': '/route/station/%d/%d/' % (60003469, 60004588),
                'expected': expected
            }, {
                'url': '/route/station/%s/%s/' % ('Jita IV - Caldari Business Tribunal Information Center', 'Rens VI - Moon 8 - Brutor Tribe Treasury'),
                'expected': expected
            }, {
                'url': '/route/station/%s/%d/' % ('Jita IV - Caldari Business Tribunal Information Center', 60004588),
                'expected': expected
            }, {
                'url': '/route/station/%d/%s/' % (60003469, 'Rens VI - Moon 8 - Brutor Tribe Treasury'),
                'expected': expected
            }]

    def runTest(self):
        for test in self.data:
            response = self.app.get(test['url'])
            result = ''.join(response.data.split())
            self.assertEquals(test['expected'], result, test['url'])

class JumpTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.app = everest.app.test_client()

        expected = ''.join(json.dumps({ 'jumps': 15 }).split())
        self.data = [{
                'url': '/jump/%d/%d/' % (30000142, 30002510),
                'expected': expected
            }, {
                'url': '/jump/%s/%s/' % ('Jita', 'Rens'),
                'expected': expected
            }, {
                'url': '/jump/%s/%d/' % ('Jita', 30002510),
                'expected': expected
            }, {
                'url': '/jump/%d/%s/' % (30000142, 'Rens'),
                'expected': expected
            }]

    def runTest(self):
        for test in self.data:
            response = self.app.get(test['url'])
            result = ''.join(response.data.split())
            self.assertEquals(test['expected'], result, test['url'])

class JumpStationTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.app = everest.app.test_client()

        expected = ''.join(json.dumps({ 'jumps': 15 }).split())
        self.data = [{
                'url': '/jump/station/%d/%d/' % (60003469, 60004588),
                'expected': expected
            }, {
                'url': '/jump/station/%s/%s/' % ('Jita IV - Caldari Business Tribunal Information Center', 'Rens VI - Moon 8 - Brutor Tribe Treasury'),
                'expected': expected
            }, {
                'url': '/jump/station/%s/%d/' % ('Jita IV - Caldari Business Tribunal Information Center', 60004588),
                'expected': expected
            }, {
                'url': '/jump/station/%d/%s/' % (60003469, 'Rens VI - Moon 8 - Brutor Tribe Treasury'),
                'expected': expected
            }]

    def runTest(self):
        for test in self.data:
            response = self.app.get(test['url'])
            result = ''.join(response.data.split())
            self.assertEquals(test['expected'], result, test['url'])

class BatchTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.app = everest.app.test_client()

        self.data = [{ # Source is system name
            'url': '/jump/batch/',
            'json': json.dumps({ 'source': 'Jita', 'destinations': ['Rens', 'Frarn']}),
            'expected': ''.join(json.dumps({ 'source': 'Jita', 'destinations': [{ 'destination': 'Rens', 'jumps': 15}, { 'destination': 'Frarn', 'jumps': 14}]}).split())
        }, {
            'url': '/jump/batch/',
            'json': json.dumps({ 'source': 'Jita', 'destinations': [30002510, 'Frarn']}),
            'expected': ''.join(json.dumps({ 'source': 'Jita', 'destinations': [{ 'destination': 30002510, 'jumps': 15}, { 'destination': 'Frarn', 'jumps': 14}]}).split())
        }, {
            'url': '/jump/batch/',
            'json': json.dumps({ 'source': 'Jita', 'destinations': ['Rens VI - Moon 8 - Brutor Tribe Treasury', 'Frarn']}),
            'expected': ''.join(json.dumps({ 'source': 'Jita', 'destinations': [{ 'destination': 'Rens VI - Moon 8 - Brutor Tribe Treasury', 'jumps': 15}, { 'destination': 'Frarn', 'jumps': 14}]}).split())
        }, {
            'url': '/jump/batch/',
            'json': json.dumps({ 'source': 'Jita', 'destinations': [60004588, 'Frarn']}),
            'expected': ''.join(json.dumps({ 'source': 'Jita', 'destinations': [{ 'destination': 60004588, 'jumps': 15}, { 'destination': 'Frarn', 'jumps': 14}]}).split())
        }, { # Source is system ID
            'url': '/jump/batch/',
            'json': json.dumps({ 'source': 30000142, 'destinations': ['Rens', 'Frarn']}),
            'expected': ''.join(json.dumps({ 'source': 30000142, 'destinations': [{ 'destination': 'Rens', 'jumps': 15}, { 'destination': 'Frarn', 'jumps': 14}]}).split())
        }, {
            'url': '/jump/batch/',
            'json': json.dumps({ 'source': 30000142, 'destinations': [30002510, 'Frarn']}),
            'expected': ''.join(json.dumps({ 'source': 30000142, 'destinations': [{ 'destination': 30002510, 'jumps': 15}, { 'destination': 'Frarn', 'jumps': 14}]}).split())
        }, {
            'url': '/jump/batch/',
            'json': json.dumps({ 'source': 30000142, 'destinations': ['Rens VI - Moon 8 - Brutor Tribe Treasury', 'Frarn']}),
            'expected': ''.join(json.dumps({ 'source': 30000142, 'destinations': [{ 'destination': 'Rens VI - Moon 8 - Brutor Tribe Treasury', 'jumps': 15}, { 'destination': 'Frarn', 'jumps': 14}]}).split())
        }, {
            'url': '/jump/batch/',
            'json': json.dumps({ 'source': 30000142, 'destinations': [60004588, 'Frarn']}),
            'expected': ''.join(json.dumps({ 'source': 30000142, 'destinations': [{ 'destination': 60004588, 'jumps': 15}, { 'destination': 'Frarn', 'jumps': 14}]}).split())
        }, { # Source is station name
            'url': '/jump/batch/',
            'json': json.dumps({ 'source': 'Jita IV - Caldari Business Tribunal Information Center', 'destinations': ['Rens', 'Frarn']}),
            'expected': ''.join(json.dumps({ 'source': 'Jita IV - Caldari Business Tribunal Information Center', 'destinations': [{ 'destination': 'Rens', 'jumps': 15}, { 'destination': 'Frarn', 'jumps': 14}]}).split())
        }, {
            'url': '/jump/batch/',
            'json': json.dumps({ 'source': 'Jita IV - Caldari Business Tribunal Information Center', 'destinations': [30002510, 'Frarn']}),
            'expected': ''.join(json.dumps({ 'source': 'Jita IV - Caldari Business Tribunal Information Center', 'destinations': [{ 'destination': 30002510, 'jumps': 15}, { 'destination': 'Frarn', 'jumps': 14}]}).split())
        }, {
            'url': '/jump/batch/',
            'json': json.dumps({ 'source': 'Jita IV - Caldari Business Tribunal Information Center', 'destinations': ['Rens VI - Moon 8 - Brutor Tribe Treasury', 'Frarn']}),
            'expected': ''.join(json.dumps({ 'source': 'Jita IV - Caldari Business Tribunal Information Center', 'destinations': [{ 'destination': 'Rens VI - Moon 8 - Brutor Tribe Treasury', 'jumps': 15}, { 'destination': 'Frarn', 'jumps': 14}]}).split())
        }, {
            'url': '/jump/batch/',
            'json': json.dumps({ 'source': 'Jita IV - Caldari Business Tribunal Information Center', 'destinations': [60004588, 'Frarn']}),
            'expected': ''.join(json.dumps({ 'source': 'Jita IV - Caldari Business Tribunal Information Center', 'destinations': [{ 'destination': 60004588, 'jumps': 15}, { 'destination': 'Frarn', 'jumps': 14}]}).split())
        }, { # Source is station ID
            'url': '/jump/batch/',
            'json': json.dumps({ 'source': 60003469, 'destinations': ['Rens', 'Frarn']}),
            'expected': ''.join(json.dumps({ 'source': 60003469, 'destinations': [{ 'destination': 'Rens', 'jumps': 15}, { 'destination': 'Frarn', 'jumps': 14}]}).split())
        }, {
            'url': '/jump/batch/',
            'json': json.dumps({ 'source': 60003469, 'destinations': [30002510, 'Frarn']}),
            'expected': ''.join(json.dumps({ 'source': 60003469, 'destinations': [{ 'destination': 30002510, 'jumps': 15}, { 'destination': 'Frarn', 'jumps': 14}]}).split())
        }, {
            'url': '/jump/batch/',
            'json': json.dumps({ 'source': 60003469, 'destinations': ['Rens VI - Moon 8 - Brutor Tribe Treasury', 'Frarn']}),
            'expected': ''.join(json.dumps({ 'source': 60003469, 'destinations': [{ 'destination': 'Rens VI - Moon 8 - Brutor Tribe Treasury', 'jumps': 15}, { 'destination': 'Frarn', 'jumps': 14}]}).split())
        }, {
            'url': '/jump/batch/',
            'json': json.dumps({ 'source': 60003469, 'destinations': [60004588, 'Frarn']}),
            'expected': ''.join(json.dumps({ 'source': 60003469, 'destinations': [{ 'destination': 60004588, 'jumps': 15}, { 'destination': 'Frarn', 'jumps': 14}]}).split())
        }]

    def runTest(self):
        for test in self.data:
            response = self.app.post(test['url'], content_type='application/json', data=test['json'])
            result = ''.join(response.data.split())
            self.assertEquals(test['expected'], result)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(RouteTestCase())
    suite.addTest(RouteStationTestCase())
    suite.addTest(JumpTestCase())
    suite.addTest(JumpStationTestCase())
    suite.addTest(BatchTestCase())
    unittest.TextTestRunner(verbosity=2).run(suite)
