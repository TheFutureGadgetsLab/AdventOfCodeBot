from logging import critical, debug, error, info, warning

from src.Player import Player
from src.utils import get_stars, query_leaderboard_API, truncate_name

HEADER = """
Day                1111111111222222
          1234567890123456789012345\
"""

class Leaderboard:
    def __init__(self, db) -> None:
        self.players = []

        self.query_leaderboard()
        self.merge_shelf(db)

    def query_leaderboard(self):
        data = query_leaderboard_API()['members']
        for person in data.values():
            self.players.append(Player(person))
        self.players = sorted(self.players, key=lambda player: player.score, reverse=True)

    def custom_leaderboard(self):
        return self.build_embed(self.custom_scores())
    
    def custom_scores(self):
        scores = {player: 0 for player in self.players}
        for day in range(0,25):
            part1 = sorted([
                (player, player.days[day].part1_time) for player in self.players if player.days[day].part1_time
            ], key=lambda tup: tup[-1])
            part2 = sorted([
                (player, player.days[day].part2_time) for player in self.players if player.days[day].part2_time
            ], key=lambda tup: tup[-1])
            for pos, (player, _) in enumerate(part1):
                scores[player] += len(self.players) - pos
            for pos, (player, _) in enumerate(part2):
                scores[player] += len(self.players) - pos

        return {k:v for k, v in sorted(scores.items(), key=lambda entry: entry[-1], reverse=True)}
    
    def players_sorted_public(self):
        return sorted(self.players, key=lambda player: player.score, reverse=True)
    
    def players_sorted_custom(self):
        scores = self.custom_scores()
        return sorted(self.players, key=lambda player: scores[player], reverse=True)

    def public_leaderboard(self) -> str:
        return self.build_embed({player: player.score for player in self.players})

    def build_embed(self, scores: dict):
        ls = [HEADER]
        for pos, (player, score) in enumerate(scores.items()):
            ls.append(f"{pos: 3}) {score: 4} {get_stars(player)} {truncate_name(player.name)}")
        return "```\n{}```".format("\n".join(ls))

    def merge_shelf(self, db):
        registered_players = [x['username'].lower() for x in db.values()]
        inverted_db = {v['username'].lower(): {'start_times': v['start_times'], 'discord': k} for k,v in db.items()}
        for player in self.players:
            if player.name.lower() not in registered_players:
                debug(f"in merge_self: '{player.name}' is not in registered_players")
                continue

            player.discord = inverted_db[player.name.lower()]['discord']
            for problem in player.days:
                if(inverted_db[player.name.lower()]['start_times'][problem.day-1]):
                    problem.start_time = inverted_db[player.name.lower()]['start_times'][problem.day-1]
