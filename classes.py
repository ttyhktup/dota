from dataclasses import dataclass
from typing import Optional

@dataclass
class PlayerMatch:
    match_id: int
    player_slot: int
    radiant_win: bool
    duration: int
    game_mode: int
    lobby_type: int
    start_time: int
    hero_id: int
    version: Optional[int] = None
    kills: int = 0
    deaths: int = 0
    assists: int = 0
    leaver_status: int = 0
    party_size: Optional[int] = None
    average_rank: int = 0
    hero_variant: int = 0
    item_0: int = 0
    item_1: int = 0
    item_2: int = 0
    item_3: int = 0
    item_4: int = 0
    item_5: int = 0

@dataclass
class Hero:
    id: int
    name: str
    localized_name: str
    primary_attr: str
    attack_type: str
    roles: list
    legs: int

    
