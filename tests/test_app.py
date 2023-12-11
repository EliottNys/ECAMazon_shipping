# test_app.py
import pytest
from app import app, mongo
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        with app.app_context():
            # Vous pouvez ajouter ici une initialisation de la base de données si nécessaire
            pass
        yield test_client

@patch('app.get_user_address')
@patch('app.send_to_dispatching')
def test_new_parcel(mock_send_to_dispatching, mock_get_user_address, client):
    # Simuler une réponse pour get_user_address
    mock_get_user_address.return_value = 'Test Address'

    # Données pour la requête POST
    parcel_data = {'order_id': '123', 'user_id': '456', 'parcel_id': '789'}

    # Envoyer la requête POST
    response = client.post('/new_parcel', json=parcel_data)

    # Vérifier le code de statut de la réponse
    assert response.status_code == 200
    assert b'Parcel information received successfully' in response.data

    # Vérifier que send_to_dispatching a été appelé
    mock_send_to_dispatching.assert_called_with('789', 'Test Address')

def test_all_parcels(client):
    # Envoyer une requête GET à la route /all_parcels
    response = client.get('/all_parcels')

    # Vérifier le code de statut de la réponse
    assert response.status_code == 200
    # Ajoutez des assertions supplémentaires basées sur le contenu de votre template 'all_parcels.html'

@patch('app.mongo.db.parcels.find_one')
def test_get_parcel_info(mock_find_one, client):
    # Configurer le mock pour simuler une réponse de la base de données
    mock_find_one.return_value = {'parcel_id': '123', 'order_id': '456', 'user_id': '789', 'address': 'Test Address', 'status': 'Processing'}

    # Envoyer une requête GET
    response = client.get('/parcel/123')

    # Vérifier le code de statut de la réponse
    assert response.status_code == 200
    # Ajoutez des assertions supplémentaires basées sur le contenu de votre template 'parcel.html'
