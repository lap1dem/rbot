import random
from typing import Iterable
from src.civ5draft.data.civ_dict import civ_dict

ALL_NATIONS = list(set(civ_dict.values()))


class Draft:
    def __init__(self, players: Iterable[int], num_nations: int = 3, banned: Iterable[str] = []):
        self.players = players
        self.num_nations = num_nations
        self.banned = banned
        self.drafted_nations = {player: None for player in self.players}
        self._draft()

    def _draft(self):
        all_nations = ALL_NATIONS.copy()
        for bn in self.banned:
            if bn in all_nations:
                all_nations.remove(bn)
            else:
                print(f"Could not find {bn} in list of nations.")

        for player in self.players:
            players_draft = random.sample(all_nations, self.num_nations)
            self.drafted_nations[player] = players_draft

            for drafted_nation in players_draft:
                all_nations.remove(drafted_nation)
