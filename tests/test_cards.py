import pytest
import requests
import json

from config import Config
from utils.response_helpers import debug_response
from utils.response_helpers import print_object
from utils.response_helpers import debug_auth_inputs


@pytest.mark.positive
def test_create_card(board_factory, list_factory, card_factory):
    board_response = board_factory("Test")
    board_data = board_response.json()

    list_response = list_factory(board_data['id'],"To-Do")
    list_data = list_response.json()

    card_response = card_factory(list_data['id'],"Card 1")
    card_data = card_response.json()
    #print(json.dumps(card_data, indent=2, sort_keys=True))
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
    #debug_auth_inputs(key,token)
    #debug_response(card_response)

    error_text = card_response.text.lower()
    assert board_response.status_code == 200
    assert list_response.status_code == 200
    assert card_response.status_code == 401
    assert "missing" in error_text or "invalid" in error_text


@pytest.mark.positive
@pytest.mark.working
def test_card_full_crud_workflow(board_factory, list_factory):
    board_response = board_factory("Test")
    board_data = board_response.json()

    list_response_todo = list_factory(board_data['id'],"To-Do")
    list_data_todo = list_response_todo.json()
    list_response_done = list_factory(board_data['id'],"Done")
    list_data_done = list_response_done.json()

    assert board_response.status_code == 200
    assert list_response_todo.status_code == 200
    assert list_response_done.status_code == 200

# -----Create Card Test phase-------

    create_url = f"{Config.BASE_URL}/cards"

    create_query = {
        'name': 'Card 1',
        'idList': list_data_todo['id'],
        'key': Config.TRELLO_KEY,
        'token': Config.TRELLO_TOKEN,
        'desc': "Initial description"
    }

    create_card_response = requests.post(create_url, params=create_query)
    create_card_data = create_card_response.json()
    #print_object(card_data)

    assert create_card_response.status_code == 200

    #1). Structure: Response has the correct shape
    assert 'name' in create_card_data
    assert 'id' in create_card_data
    assert 'idList' in create_card_data
    assert 'idBoard' in create_card_data
    assert 'badges' in create_card_data
    assert 'desc' in create_card_data

    #2). Schema Validation: Response has correct data types
    assert isinstance(create_card_data['name'], str)
    assert isinstance(create_card_data['id'], str)
    assert isinstance(create_card_data['idList'], str)
    assert isinstance(create_card_data['idBoard'], str)
    assert isinstance(create_card_data['desc'], str)
    assert isinstance(create_card_data['badges'], dict)
    assert isinstance(create_card_data['closed'], bool)

    #3). Data Integrity: Values match what we expect
    assert create_card_data['name'] == 'Card 1'
    assert create_card_data['idList'] == list_data_todo['id']
    assert create_card_data['idBoard'] == board_data['id']
    assert create_card_data['desc'] == 'Initial description'

    #4). Business Rules
    assert create_card_data['closed'] is False
    assert create_card_data['badges']['comments'] == 0

#----Update Card Test Phase------

    update_url = f"{Config.BASE_URL}/cards/{create_card_data['id']}"
    update_query = {
        'key': Config.TRELLO_KEY,
        'token': Config.TRELLO_TOKEN,
        'desc': "New description"
    }

    update_card_response = requests.put(update_url, params= update_query)
    update_card_data = update_card_response.json()
    #print_object(card_data)

    assert update_card_response.status_code == 200

    # 1). Structure: Response has the correct shape
    assert 'name' in update_card_data
    assert 'id' in update_card_data
    assert 'idList' in update_card_data
    assert 'idBoard' in update_card_data
    assert 'desc' in update_card_data
    assert 'closed'in update_card_data
    assert 'badges' in update_card_data

    # 2). Schema Validation: Response has correct data types
    assert isinstance(update_card_data['name'], str)
    assert isinstance(update_card_data['id'], str)
    assert isinstance(update_card_data['idList'], str)
    assert isinstance(update_card_data['idBoard'], str)
    assert isinstance(update_card_data['desc'], str)
    assert isinstance(update_card_data['closed'], bool)
    assert isinstance(update_card_data['badges'], dict)

    # 3). Data Integrity: Values match what we expect
    assert update_card_data['name'] == 'Card 1'
    assert update_card_data['idBoard'] == board_data['id']
    assert update_card_data['desc'] == 'New description'

    # 4). Business Rules
    assert update_card_data['closed'] is False
    assert update_card_data['badges']['comments'] == 0
#----Move Card Phase-----

    move_url = f"{Config.BASE_URL}/cards/{create_card_data['id']}"
    move_query = {
        'key': Config.TRELLO_KEY,
        'token': Config.TRELLO_TOKEN,
        'idList': list_data_done['id'],
    }

    move_card_response = requests.put(move_url, params= move_query)
    move_card_data = move_card_response.json()
    #print_object(move_card_data)

    # 1). Structure: Response has the correct shape
    assert 'name' in move_card_data
    assert 'id' in move_card_data
    assert 'idList' in move_card_data
    assert 'idBoard' in move_card_data
    assert 'desc' in move_card_data
    assert 'closed'in move_card_data
    assert 'badges' in move_card_data

    # 2). Schema Validation: Response has correct data types
    assert isinstance(move_card_data['name'], str)
    assert isinstance(move_card_data['id'], str)
    assert isinstance(move_card_data['idList'], str)
    assert isinstance(move_card_data['idBoard'], str)
    assert isinstance(move_card_data['desc'], str)
    assert isinstance(move_card_data['closed'], bool)
    assert isinstance(move_card_data['badges'], dict)

    # 3). Data Integrity: Values match what we expect
    assert move_card_data['name'] == 'Card 1'
    assert move_card_data['idBoard'] == board_data['id']
    assert move_card_data['idList'] == list_data_done['id']

    # 4). Business Rules
    assert move_card_data['closed'] is False
    assert move_card_data['badges']['comments'] == 0

#----Delete Card Phase----
    deleted_card_id = move_card_data['id']
    url = f"{Config.BASE_URL}/cards/{move_card_data['id']}"
    query = {
        'key': Config.TRELLO_KEY,
        'token': Config.TRELLO_TOKEN,
    }

    delete_card_response = requests.delete(url, params= query)
    delete_card_data = delete_card_response.json()
    #print_object(card_data)

    assert delete_card_response.status_code == 200

    url = f"{Config.BASE_URL}/cards/{deleted_card_id}"
    query = {
        'key': Config.TRELLO_KEY,
        'token': Config.TRELLO_TOKEN,
    }

    get_card_response = requests.get(url, params= query)
    #debug_response(card_response)
    error_text = get_card_response.text.lower()

    assert get_card_response.status_code == 404
    assert "not found" in error_text

