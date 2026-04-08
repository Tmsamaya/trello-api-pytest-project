import pytest
import json


@pytest.mark.positive
def test_create_board(board_factory):
    response = board_factory("Test")
    data = response.json()
    #print(json.dumps(response.json(), indent=2, sort_keys=True))

    assert response.status_code == 200
    assert data['closed'] is False

@pytest.mark.positive
def test_create_list(board_factory, list_factory):
    board_response = board_factory("Test")
    board_data = board_response.json()

    list_response = list_factory(board_data['id'],"To-Do")
    list_data = list_response.json()
    # print(json.dumps(list_data, indent=2, sort_keys=True))

    assert board_response.status_code == 200
    assert list_response.status_code == 200
    assert list_data['name'] == "To-Do"
    assert list_data['idBoard'] == board_data['id']
