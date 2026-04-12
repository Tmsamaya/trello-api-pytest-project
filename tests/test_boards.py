import pytest
import json
from utils.response_helpers import debug_response


@pytest.mark.positive
def test_create_board(board_factory):
    response = board_factory("Test")
    #debug_response(response)
    data = response.json()
    #print(json.dumps(response.json(), indent=2, sort_keys=True))

    assert response.status_code == 200
    assert data['closed'] is False


