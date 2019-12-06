import league
champion_dict = league.get_champion_dict()

async def parse_game_data(game_data, summoner_id):
    participant_list = game_data['participants']
    summoners_team_id = find_summoner_team(participant_list, summoner_id)
    opponents = get_opponents(participant_list, summoners_team_id)
    opponent_string =  "-----------------------------\n"
    opponent_string += "-----------------------------\n"
    for opponent_id, champion_id, opponent_name in opponents:
        opponent_rank = league.get_summoner_data(opponent_id)
        champion_name = champion_dict[champion_id]
        opponent_string += f"{champion_name} - {opponent_name}\n"
        for rank in opponent_rank:
            opponent_string += f"{rank['Queue']}: {rank['Rank']} {rank['Win-rate']} W/L\n"
        opponent_string += "-----------------------------\n"
    opponent_string += "-----------------------------\n"
    return opponent_string



def find_summoner_team(participant_list, summoner_id):
    for participant in participant_list:
        if participant['summonerId'] == summoner_id:
            return participant['teamId']


def get_opponents(participant_list, ally_team_id):
    opponents = []
    for participant in participant_list:
        if participant['teamId'] != ally_team_id:
            opp_info = (
                participant['summonerId'], participant['championId'], participant['summonerName']
            )
            opponents.append(opp_info)
    return opponents
