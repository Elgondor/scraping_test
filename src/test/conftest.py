import pytest
import sys
# sys.path.append(".")
from ..apps import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client