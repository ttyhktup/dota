import api
import json

# find pick time and order for every game (match) for wraith king for player 212946967 and write into file as json. last 500 games only.

# filter last 500 games by date
# find matches with wraith king for player 212946967
# find what hero level was at 10 minutes
# put info in json file

playerMatches = api.getPlayerMatches(limit = 500, sort="start_time")

heroes = api.getHeroes()

hero_id = None

for hero in heroes:
    if hero.localized_name == "Wraith King":
        hero_id = hero.id
        break

playerMatches = [match for match in playerMatches if match.hero_id == hero_id]

def xp_to_level(xp):
    xp_table = [0, 230, 610, 1080, 1660, 2260, 2980, 3730, 4610, 5610,
                6730, 7990, 9390, 10930, 12630, 14480, 16480, 18630,
                20930, 23380, 25980, 28730, 31630, 34680, 37880, 41230,
                44730, 48380, 52180, 56130]  # Level 1–30

    for level, required_xp in enumerate(xp_table, start=1):
        if xp < required_xp:
            return level - 1
    return 30 

def get_hero_level_at_minute_10(match_id):
    player = api.getPlayer(match_id)
    if player:
        xp_t = player.get("xp_t", [])
        if len(xp_t) > 10:
            xp_at_10 = xp_t[10]
            return xp_to_level(xp_at_10)
    return None

result = {}
for match in playerMatches:
    result[match.match_id] = get_hero_level_at_minute_10(match.match_id)


def save_result_to_file(result_dict, filename="result.json"):
    with open(filename, "w") as f:
        json.dump(result_dict, f, indent=4)


save_result_to_file(result)

