import os
import app
import unittest
import json

import app

BASE_URL = 'http://127.0.0.1:5000/task'

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True
        os.environ["UNIT_TEST"] = "True"
        with app.app.app_context():
            app.init_db()

    def test_post(self):
        post_datas = [{'name':'this_is_test1', 'status':1},
                      {'name':'this_is_test2'},
                      {'name':'this_is_test3', 'status':0},
                      {'status':0},  # 400 case
                      {'name':'this_is_test4', 'status':3},] # 400 case
        post_data = post_datas[0]
        response = self.app.post(BASE_URL,
                                data=json.dumps(post_data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data)['result']['name'], post_data['name'])
        self.assertEqual(json.loads(response.data)['result']['status'], post_data['status'])

        post_data = post_datas[1]
        response = self.app.post(BASE_URL,
                                data=json.dumps(post_data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data)['result']['name'], post_data['name'])
        self.assertEqual(json.loads(response.data)['result']['status'], 0)

        post_data = post_datas[2]
        response = self.app.post(BASE_URL,
                                data=json.dumps(post_data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data)['result']['name'], post_data['name'])
        self.assertEqual(json.loads(response.data)['result']['status'], post_data['status'])

        post_data = post_datas[3]
        response = self.app.post(BASE_URL,
                                data=json.dumps(post_data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)

        post_data = post_datas[4]
        response = self.app.post(BASE_URL,
                                data=json.dumps(post_data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_get_all(self):
        with app.app.app_context():
            count = len(app.query_db('select * from Table1;'))
        response = self.app.get(BASE_URL)
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data['result']), count)

    def test_update(self):
        put_datas = [{'id': 1, 'name':'this_is_puttest', 'status':1},
                     {'id': 1,'name':'this_is_puttest2', 'status':0},
                      {'id': 1, 'status':1},
                      {'id': 1, 'name':'this_is_puttest3'},
                      {'id': 1, 'name':'this_is_test3', 'status':2}, # 400
                      {'id': 0, 'name':'this_is_test3', 'status':1}, # 400
                      {'id': 1, 'name': ""}]  #400
        put_data = put_datas[0]
        response = self.app.put(BASE_URL,
                                data=json.dumps(put_data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['result']['name'], put_data['name'])
        self.assertEqual(json.loads(response.data)['result']['status'], put_data['status'])

        put_data = put_datas[1]
        response = self.app.put(BASE_URL,
                                data=json.dumps(put_data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['result']['name'], put_data['name'])
        self.assertEqual(json.loads(response.data)['result']['status'], put_data['status'])

        pre_put_data = put_data
        put_data = put_datas[2]
        response = self.app.put(BASE_URL,
                                data=json.dumps(put_data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['result']['name'], pre_put_data['name'])
        self.assertEqual(json.loads(response.data)['result']['status'], put_data['status'])

        pre_put_data = put_data
        put_data = put_datas[3]
        response = self.app.put(BASE_URL,
                                data=json.dumps(put_data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['result']['name'], put_data['name'])
        self.assertEqual(json.loads(response.data)['result']['status'], pre_put_data['status'])

        for put_data in put_datas[4:]:
            response = self.app.put(BASE_URL,
                                    data=json.dumps(put_data),
                                    content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_delete(self):
        response = self.app.delete(BASE_URL,
                                data=json.dumps({'id':0}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
        # Get last id
        with app.app.app_context():
            last_id = app.query_db('select * from Table1;')[-1]['id']
        response = self.app.delete(BASE_URL,
                                data=json.dumps({'id': last_id}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        os.environ["UNIT_TEST"] = "False"

if __name__ == '__main__':
    unittest.main()