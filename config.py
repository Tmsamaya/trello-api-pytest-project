import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    TRELLO_KEY = os.getenv("TRELLO_KEY")
    TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
    Base_Url = "https://api.trello.com/1"