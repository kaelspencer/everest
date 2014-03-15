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

class IndustryTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.app = everest.app.test_client()

        self.data = [{
            'url': '/industry/detail/names/3655/',
            'expected': ''.join(json.dumps({'items': {'3655': {'categoryName': 'Module', 'chance': 0.4, 'datacores': [{'quantity': 2, 'typeID': 20415, 'typeName': 'Datacore - Molecular Engineering'}, {'quantity': 2, 'typeID': 20424, 'typeName': 'Datacore - Mechanical Engineering'}], 'decryptor_category': 729, 'maxProductionLimit': 100, 'perfectMaterials': [{'dmg': 1.0, 'name': 'Tritanium', 'quantity': 160.0, 'typeID': 34, 'wasteME': True, 'wastePE': True }, {'dmg': 1.0, 'name': 'Pyerite', 'quantity': 1266.0, 'typeID': 35, 'wasteME': True, 'wastePE': True }, {'dmg': 1.0, 'name': 'Zydrine', 'quantity': 2.0, 'typeID': 39, 'wasteME': True, 'wastePE': True }, {'dmg': 1.0, 'name': 'Megacyte', 'quantity': 3.0, 'typeID': 40, 'wasteME': True, 'wastePE': True }, {'dmg': 1.0, 'name': 'Morphite', 'quantity': 3.0, 'typeID': 11399, 'wasteME': True, 'wastePE': True }, {'dmg': 1.0, 'name': 'Medium Hull Repairer I', 'quantity': 1.0, 'typeID': 3653, 'wasteME': False, 'wastePE': False }, {'dmg': 1.0, 'name': 'Robotics', 'quantity': 4.0, 'typeID': 9848, 'wasteME': False, 'wastePE': False }, {'dmg': 0.25, 'name': 'R.A.M.- Armor/Hull Tech', 'quantity': 1.0, 'typeID': 11475, 'wasteME': False, 'wastePE': False }, {'dmg': 1.0, 'name': 'Nanomechanical Microprocessor', 'quantity': 2.0, 'typeID': 11538, 'wasteME': False, 'wastePE': False }], 'productionTime': 6000, 'productivityModifier': 1200, 't1bpo': {'blueprintTypeID': 3654, 'maxProductionLimit': 300, 'researchCopyTime': 12000, 'typeID': 3653, 'typeName': 'Medium Hull Repairer I'}, 'typeID': 3655, 'typeName': 'Medium Hull Repairer II', 'wasteFactor': 10 } } }).split())
        }, {
            'url': '/industry/detail/11957/',
            'expected': ''.join(json.dumps({'items': {'11957': {'categoryName': 'Ship', 'chance': 0.25, 'datacores': [{'quantity': 8, 'typeID': 20424 }, {'quantity': 8, 'typeID': 25887 }], 'decryptor_category': 731, 'maxProductionLimit': 10, 'perfectMaterials': [{'dmg': 1.0, 'quantity': 50.0, 'typeID': 3828, 'wasteME': True, 'wastePE': True }, {'dmg': 1.0, 'quantity': 100.0, 'typeID': 11399, 'wasteME': True, 'wastePE': True }, {'dmg': 1.0, 'quantity': 38.0, 'typeID': 11533, 'wasteME': True, 'wastePE': True }, {'dmg': 1.0, 'quantity': 330.0, 'typeID': 11534, 'wasteME': True, 'wastePE': True }, {'dmg': 1.0, 'quantity': 1200.0, 'typeID': 11540, 'wasteME': True, 'wastePE': True }, {'dmg': 1.0, 'quantity': 2500.0, 'typeID': 11544, 'wasteME': True, 'wastePE': True }, {'dmg': 1.0, 'quantity': 20.0, 'typeID': 11550, 'wasteME': True, 'wastePE': True }, {'dmg': 1.0, 'quantity': 250.0, 'typeID': 11552, 'wasteME': True, 'wastePE': True }, {'dmg': 1.0, 'quantity': 200.0, 'typeID': 11558, 'wasteME': True, 'wastePE': True }, {'dmg': 1.0, 'quantity': 1.0, 'typeID': 632, 'wasteME': False, 'wastePE': False }, {'dmg': 0.95, 'quantity': 12.0, 'typeID': 11478, 'wasteME': False, 'wastePE': False }], 'productionTime': 120000, 'productivityModifier': 24000, 't1bpo': {'blueprintTypeID': 977, 'maxProductionLimit': 15, 'researchCopyTime': 240000, 'typeID': 632 }, 'typeID': 11957, 'typeName': 'Falcon', 'wasteFactor': 10 } } }).split())
        }, {
            'url': '/industry/detail/0/',
            'expected': ''.join(json.dumps({'items': {} }).split())
        }]

    def runTest(self):
        for test in self.data:
            response = self.app.get(test['url'])
            result = ''.join(response.data.split())
            self.assertEquals(test['expected'], result)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(RouteTestCase())
    suite.addTest(RouteStationTestCase())
    suite.addTest(JumpTestCase())
    suite.addTest(JumpStationTestCase())
    suite.addTest(BatchTestCase())
    suite.addTest(IndustryTestCase())
    unittest.TextTestRunner(verbosity=2).run(suite)
