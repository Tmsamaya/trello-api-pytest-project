import pytest
import json
from utils.response_helpers import debug_response
from utils.response_helpers import print_object
from utils.response_helpers import debug_auth_inputs


@pytest.mark.positive
@pytest.mark.working
def test_create_card(board_factory, list_factory, card_factory):
    board_response = board_factory("Test")
    board_data = board_response.json()

    list_response = list_factory(board_data['id'],"To-Do")
    list_data = list_response.json()

    card_response = card_factory(list_data['id'],"Card 1")
    card_data = card_response.json()
    print(json.dumps(card_data, indent=2, sort_keys=True))
    #print(json.dumps(list_data, indent=2, sort_keys=True))

    assert board_response.status_code == 200
    assert list_response.status_code == 200
    assert card_response.status_code == 200

    #1). Structure: Response has the correct shape
    assert 'name' in card_data
    assert 'id' in card_data
    assert 'idList' in card_data
    assert 'idBoard' in card_data
    assert 'badges' in card_data

    #2). Schema Validation: Response has correct data types
    assert isinstance(card_data['name'], str)
    assert isinstance(card_data['id'], str)
    assert isinstance(card_data['idList'], str)
    assert isinstance(card_data['idBoard'], str)
    assert isinstance(card_data['badges'], dict)
    assert isinstance(card_data['closed'], bool)

    #3). Data Integrity: Values match what we expect
    assert card_data['name'] == 'Card 1'
    assert card_data['idList'] == list_data['id']
    assert card_data['idBoard'] == board_data['id']

    #4). Business Rules
    assert card_data['closed'] is False
    assert card_data['badges']['comments'] == 0



@pytest.mark.negative
def test_create_card_with_invalid_list_id(board_factory, list_factory, card_factory):
    board_response = board_factory("Test")
    board_data = board_response.json()

    list_response = list_factory(board_data['id'],"To-Do")
    list_data = list_response.json()

    card_response = card_factory('',"Card 1")
    card_data = card_response.text


    assert board_response.status_code == 200
    assert list_response.status_code == 200
    assert card_response.status_code == 400



@pytest.mark.negative
@pytest.mark.parametrize (
    "key, token",
    [
    pytest.param("", None, id ="Missing APIKey"),
    pytest.param("56565", None, id="Bad APIKey"),
    pytest.param(None, "", id="Missing Token"),
    pytest.param(None, "45454", id="Bad Token"),
    ]
)
def test_create_card_with_invalid_auth(board_factory, list_factory, card_factory, key, token):
    board_response = board_factory("Test")
    board_data = board_response.json()

    list_response = list_factory(board_data['id'],"To-Do")
    list_data = list_response.json()

    card_response = card_factory(list_data['id'], "Card 1",key=key, token=token)
    debug_auth_inputs(key,token)
    debug_response(card_response)

    error_text = card_response.text.lower()
    assert board_response.status_code == 200
    assert list_response.status_code == 200
    assert card_response.status_code == 401

    assert "missing" in error_text or "invalid" in error_text