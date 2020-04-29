import pytest
import searchapp.searchapp as search_app


@pytest.fixture
def client():
    search_app.app.config['TESTING'] = True
    return search_app.app.test_client()
