import requests
from tqdm import tqdm
from api_key import api_key
from classes import PlayerMatch, Hero

base_url = 'https://api.opendota.com/api'
account_id = 212946967

def getPlayerMatches(limit=None, sort=None):
    url = f'{base_url}/players/{account_id}/matches?api_key={api_key}&limit={limit}&sort={sort}'
    response = requests.get(url)
    matches = [PlayerMatch(**match) for match in response.json()]
    return matches

def makeMatchesParsed(matches):
    for match in tqdm(matches):
        if match.version == None:
            url = f'{base_url}/request/{match.match_id}?api_key={api_key}'
            response = requests.post(url)
            if response.status_code != 200:
                raise Exception(f"Something went wrong: {response.status_code} {response.json()}")

def checkParsed(matches):
    for match in matches:
        if match.version == None:
            raise Exception(f"Match version: {match.version}")
        return "Success!!! Dabl-u"

def getHeroes():
    url = f'{base_url}/heroes?api_key={api_key}'
    response = requests.get(url)
    heroes = [Hero(**hero) for hero in response.json()]
    return heroes

def getPlayer(match_id):
    url = f'{base_url}/matches/{match_id}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()

    for player in data.get("players", []):
        if player.get("account_id") == account_id:
            return player
    return None 
