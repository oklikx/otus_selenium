# src/tests/test_customer_db.py
import uuid
import pytest
from lib.db import create_customer, get_customer_by_id, update_customer, delete_customer


@pytest.fixture
def sample_customer_data():
    unique_id = str(uuid.uuid4())[:8]
    return {
        "firstname": "Test",
        "lastname": "User",
        "email": f"test_{unique_id}@example.com",
        "passwd": "secret",
    }


def test_create_customer(db_connection, sample_customer_data):
    customer_id = create_customer(db_connection, sample_customer_data)
    assert customer_id is not None
    assert customer_id > 0
    customer = get_customer_by_id(db_connection, customer_id)
    assert customer is not None
    assert customer['firstname'] == sample_customer_data['firstname']
    assert customer['lastname'] == sample_customer_data['lastname']
    assert customer['email'] == sample_customer_data['email']


def test_update_customer(db_connection, sample_customer_data):
    customer_id = create_customer(db_connection, sample_customer_data)
    update_data = {
        "firstname": "UpdatedName",
        "lastname": "UpdatedLast",
        "email": f"updated_{customer_id}@example.com",
    }
    affected = update_customer(db_connection, customer_id, update_data)
    assert affected == 1
    updated = get_customer_by_id(db_connection, customer_id)
    assert updated['firstname'] == update_data['firstname']
    assert updated['lastname'] == update_data['lastname']
    assert updated['email'] == update_data['email']


def test_update_nonexistent_customer(db_connection):
    non_existent_id = 999999999
    affected = update_customer(db_connection, non_existent_id, {
                               "firstname": "Ghost"})
    assert affected == 0


def test_delete_customer(db_connection, sample_customer_data):
    customer_id = create_customer(db_connection, sample_customer_data)
    assert get_customer_by_id(db_connection, customer_id) is not None
    affected = delete_customer(db_connection, customer_id)
    assert affected == 1
    assert get_customer_by_id(db_connection, customer_id) is None


def test_delete_nonexistent_customer(db_connection):
    non_existent_id = 999999999
    affected = delete_customer(db_connection, non_existent_id)
    assert affected == 0
