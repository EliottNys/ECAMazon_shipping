import json
import unittest
import mongomock
from app import app, mongo
from unittest.mock import patch

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.mock_db = mongomock.MongoClient().db

    def tearDown(self):
        pass

    @mongomock.patch(servers=(('localhost', 27017),))
    @patch('app.get_user_address', return_value='Some Address')
    @patch('app.send_to_dispatching')
    def test_new_parcel(self, mock_send_to_dispatching, mock_get_user_address):
        mongo.db = self.mock_db
        response = self.app.post('/new_parcel', data=json.dumps({
            'order_id': '123',
            'user_id': '456',
            'parcel_id': '789'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        mock_get_user_address.assert_called_once_with('456')
        mock_send_to_dispatching.assert_called_once_with('789', 'Some Address')

    @mongomock.patch(servers=(('localhost', 27017),))
    def test_all_parcels(self):
        mongo.db = self.mock_db
        response = self.app.get('/all_parcels')
        self.assertEqual(response.status_code, 200)

    @mongomock.patch(servers=(('localhost', 27017),))
    def test_get_parcel_info(self):
        mongo.db = self.mock_db
        mongo.db.parcels.insert_one({'parcel_id': '123', 'order_id': '123', 'user_id': '456', 'address': 'Some Address', 'status': 'Processing'})
        response = self.app.get('/parcel/123')
        self.assertEqual(response.status_code, 200)

    @mongomock.patch(servers=(('localhost', 27017),))
    def test_new_parcel_missing_data(self):
        mongo.db = self.mock_db
        response = self.app.post('/new_parcel', data=json.dumps({
            'order_id': '123',
            'user_id': '456'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
