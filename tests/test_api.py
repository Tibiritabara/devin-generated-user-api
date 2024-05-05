import requests

BASE_URL = 'http://localhost:8000/users'


def test_create_user():
    response = requests.post(f'{BASE_URL}/', json={'name': 'John Doe', 'email': 'johndoe@example.com'})
    assert response.status_code == 200
    assert response.json()['name'] == 'John Doe'


def test_retrieve_user():
    user_id = 1  # Assuming the user with ID 1 exists
    response = requests.get(f'{BASE_URL}/{user_id}')
    assert response.status_code == 200
    assert response.json()['id'] == user_id


def test_update_user():
    user_id = 1  # Assuming the user with ID 1 exists
    new_email = 'john.doe@updatedexample.com'
    response = requests.put(f'{BASE_URL}/{user_id}', json={'email': new_email})
    assert response.status_code == 200
    assert response.json()['email'] == new_email


def test_delete_user():
    user_id = 1  # Assuming the user with ID 1 exists
    response = requests.delete(f'{BASE_URL}/{user_id}')
    assert response.status_code == 200
    assert 'detail' not in response.json()

