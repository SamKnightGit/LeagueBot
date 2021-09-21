import requests
import secret
import json

VERSION_URL = "https://ddragon.leagueoflegends.com/realms/euw.json"
BASE_URL = "https://euw1.api.riotgames.com"
SUMMONER_BY_NAME = BASE_URL + "/lol/summoner/v4/summoners/by-name/"
GAME_BY_SUMMONER = BASE_URL + "/lol/spectator/v4/active-games/by-summoner/"
ENTRY_BY_SUMMONER = BASE_URL + "/lol/league/v4/entries/by-summoner/"
headers = {
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Riot-Token": secret.RIOT_API_TOKEN,
    "Accept-Language": "en-US,en;q=0.5",
}


def get_champion_url():
    request_data = requests.get(VERSION_URL)
    if request_data.status_code == 404:
        return None
    request_data = request_data.json()
    version = request_data['v']
    return "http://ddragon.leagueoflegends.com/cdn/" + version + "/data/en_US/champion.json"


def get_champion_dict():
    champion_dict = {}
    url = get_champion_url()
    if url is None:
        return None
    request_data = requests.get(url)
    if request_data.status_code == 404:
        return None
    request_data = request_data.json()['data']
    for champion in request_data:
        champion_info = request_data[champion]
        champion_dict[int(champion_info['key'])] = champion_info['id']
    return champion_dict


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


def get_summoner_data(summoner_id):
    request_data = requests.get(
        ENTRY_BY_SUMMONER + summoner_id,
        headers=headers
    )
    if request_data.status_code == 404:
        return None
    else:
        summoner_data = request_data.json()
        result = []
        for queue in summoner_data:
            if queue["queueType"] == "RANKED_FLEX_SR":
                queue_type = "Flex"
            elif queue["queueType"] == "RANKED_SOLO_5x5":
                queue_type = "Solo"
            else:
                continue
            win_rate = (float(queue['wins']) / (queue['wins'] + queue['losses'])) * 100
            win_rate = round(win_rate, 2)
            result.append({
                "Queue": queue_type,
                "Rank": f"{queue['tier']} {queue['rank']}",
                "Win-rate": f"{win_rate}%"
            })
        print(result)
        return result


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
