import api
import json
from tqdm import tqdm

# find pick time and order for every game (match) for wraith king for player 212946967 and write into file as json. last 500 games only.

# filter last 500 games by date
# find matches with wraith king for player 212946967
# find what hero level was at 10 minutes
# put info in json file

# playerMatches = api.getPlayerMatches(212946967, limit = 500, sort="start_time")

heroes = api.getHeroes()

def find_hero_id(hero_name):
    hero_id = None
    for hero in heroes:
        if hero.localized_name == hero_name:
            hero_id = hero.id
    return hero_id

# wraith_king_id = find_hero_id("Wraith King")

# playerMatches = [match for match in playerMatches if match.hero_id == wraith_king_id]

def xp_to_level(xp):
    xp_table = [0, 230, 610, 1080, 1660, 2260, 2980, 3730, 4610, 5610,
                6730, 7990, 9390, 10930, 12630, 14480, 16480, 18630,
                20930, 23380, 25980, 28730, 31630, 34680, 37880, 41230,
                44730, 48380, 52180, 56130] 

    for level, required_xp in enumerate(xp_table, start=1):
        if xp < required_xp:
            return level - 1
    return 30 

def get_hero_level_at_minute_10(match_id, account_id):
    player = api.getPlayer(match_id, account_id)
    if player:
        xp_t = player.get("xp_t", [])
        if len(xp_t) > 10:
            xp_at_10 = xp_t[10]
            return xp_to_level(xp_at_10)
    return "No data"

def create_dictionary(playerMatches):
    result = {}
    for match in playerMatches:
        result[match.match_id] = get_hero_level_at_minute_10(match.match_id, 212946967)
    return result

def save_result_to_file(result_dict, filename="result.json"):
    with open(filename, "w") as f:
        json.dump(result_dict, f, indent=4)

# statistics of rodriga on which hero and on how many games he bought glimmer cape. optional timings.

# make list of heroes
# for each hero find the number of "glimmer capes" bought
# bonus task: add time when it was bought

#129738689, Rodr1ga
account_id = 129738689
playerMatches = api.getPlayerMatches(account_id, sort="start_time")

def sort_parsed_matches(playerMatches):
    result = []
    for match in playerMatches:
        if match.version != None:
            result.append(match)
    return result

parsedMatches = sort_parsed_matches(playerMatches)

def make_list_of_heroes(parsedMatches, heroes):

    hero_lookup = {hero.id: hero for hero in heroes}
    result = []
    
    for match in parsedMatches:
        hero_id = match.hero_id
        data = {}
        if hero_id in hero_lookup:
            data["match_id"] = match.match_id
            data["hero_name"] = hero_lookup[hero_id].localized_name
            data["hero_id"] = hero_id
            result.append(data)
    
    return result

heroes_list = make_list_of_heroes(parsedMatches, heroes)

def get_match_data(heroes_list):
    for hero in tqdm(heroes_list):
        match = api.getMatch(hero["match_id"])

        if not match or "players" not in match:
            print(f"Skipping match {hero['match_id']} — no player data available.")
            continue
        players = match["players"]

        player = next((p for p in players if p.get("account_id") == account_id), None)

        if player:
            hero["purchase"] = player.get("purchase")
            hero["purchase_log"] = player.get("purchase_log")
            hero["purchase_time"] = player.get("purchase_time")

    return heroes_list
    
match_data = get_match_data(heroes_list)

def number_of_glimmer_capes(match_data):
    for match in match_data:
        print(match)
    return

number_of_glimmer_capes(match_data)