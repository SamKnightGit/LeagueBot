import requests
import secret

BASE_URL = "https://euw1.api.riotgames.com"
SUMMONER_BY_NAME = BASE_URL + "/lol/summoner/v4/summoners/by-name/"
GAME_BY_SUMMONER = BASE_URL + "/lol/spectator/v4/active-games/by-summoner/"

headers = {
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Riot-Token": secret.RIOT_API_TOKEN,
    "Accept-Language": "en-US,en;q=0.5",
}


def get_summoner_by_name(summoner_name):
    request_data = requests.get(
        SUMMONER_BY_NAME + summoner_name,
        headers=headers
    )
    if request_data.status_code == 404:
        return None
    else:
        print(request_data.json())
        return request_data.json()


def get_current_game(summoner_id):
    request_data = requests.get(
        GAME_BY_SUMMONER + summoner_id,
        headers=headers
    )
    if request_data.status_code == 404:
        return None
    else:
        print(request_data.json())
        return request_data.json()

get_summoner_by_name("knightterror")
