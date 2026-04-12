import pytest
import requests
import json
from config import Config

@pytest.fixture
def board_factory():
    created_boards = []

    def _create_board(name=None, key=None, token=None):

        board_name = f"TestBoard" if name is None else name
        url = f"{Config.BASE_URL}/boards/"

        query = {
            'name': board_name,
            'key': Config.TRELLO_KEY if key is None else key,
            'token': Config.TRELLO_TOKEN if token is None else token
        }
        response = requests.post(url, params=query)

        if response.status_code == 200:
            board_id =response.json()['id']
            created_boards.append(board_id)

        return response

    yield _create_board

    #Teardown
    for board_id in created_boards:
        delete_url = f"{Config.BASE_URL}/boards/{board_id}"
        query = {
            'key': Config.TRELLO_KEY,
            'token': Config.TRELLO_TOKEN
        }
        response = requests.delete(delete_url, params=query)
        print(f"\nDeleting board: {board_id}")
        if response.status_code not in [200, 404]:
            print(f"\nTeardown failed for board {board_id}: {response.status_code}")


@pytest.fixture
def list_factory():
    created_lists = []

    def _create_list(board_id, name=None, key =None, token=None):

        list_name = f"TestList" if name is None else name
        url = f"{Config.BASE_URL}/lists"

        query = {
            'name': list_name,
            'idBoard': board_id,
            'key': Config.TRELLO_KEY if key is None else key,
            'token': Config.TRELLO_TOKEN if token is None else token
        }

        response = requests.post(url, params=query)

        if response.status_code == 200:
            list_id =response.json()['id']
            created_lists.append(list_id)
        return response

    yield _create_list

    for list_id in created_lists:
        delete_url = f"{Config.BASE_URL}/lists/{list_id}"
        query = {
            'key': Config.TRELLO_KEY,
            'token': Config.TRELLO_TOKEN
        }
        requests.delete(delete_url, params=query)

@pytest.fixture
def card_factory():
    created_cards = []
    def _create_card(list_id, name=None, desc=None, key=None, token=None):

        card_name = f"TestCard" if name is None else name
        url = f"{Config.BASE_URL}/cards"

        query = {
            'name': card_name,
            'idList': list_id,
            'key': Config.TRELLO_KEY if key is None else key,
            'token': Config.TRELLO_TOKEN if token is None else token
        }
        if desc is not None:
            query['desc'] = desc

        response = requests.post(url, params=query)

        if response.status_code == 200:
            card_id = response.json()['id']
            created_cards.append(card_id)
        return response

    yield _create_card

    for card_id in created_cards:
        delete_url = f"{Config.BASE_URL}/cards/{card_id}"
        query = {
            'key': Config.TRELLO_KEY,
            'token': Config.TRELLO_TOKEN
        }
        requests.delete(delete_url, params=query)

