import pytest
from videoapp.users.models import User
from videoapp.database import session

@pytest.fixture(scope='module')
def setup():
    q = session.query(User).filter_by(email='test@test.com')
    if q.count() != 0:
        q.delete(synchronize_session=False)
    session.close() 

def test_create_user(setup):
    User.create_user(email='test@test.com', password='abc123')

'''
def test_duplicate_user(setup):
    with pytest.raises(Exception):
        User.create_user(email='test@test.com', password='abc123')


def test_invalid_email(setup):
    with pytest.raises(Exception):
        User.create_user(email='test@test.com', password='abc123')
'''
        
def test_valid_password(setup):
    q = session.query(User).filter_by(email="test@test.com")
    assert q.count() == 1
    user_obj = q.first()
    assert user_obj.verify_password('abc123') == True
    assert user_obj.verify_password('abc1234') == False
    session.close()

def test_assert():
    assert True is True


def test_invalid_assert():
    with pytest.raises(AssertionError):
        assert True is not True
