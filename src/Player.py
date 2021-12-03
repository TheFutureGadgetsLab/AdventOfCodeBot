import datetime
from logging import critical, debug, error, info, warning

from tabulate import tabulate

from src.Problem import Problem
from src.utils import get_stars

HEADER = """
Day          1111111111222222
    1234567890123456789012345\
"""

class Player:
    def __init__(self, user: dict) -> None:
        self.name    = None
        self.stars   = None
        self.score   = None
        self.days    = []
        self.discord = None

        self.parse_dict(user)

        debug(f"{self.name} init'd, they have {self.stars} stars")

    def parse_dict(self, user: dict):
        self.name = user['name'] if user['name'] else f"User #{user['id']}"
        self.stars = user['stars']
        self.score = user['local_score']

        solves = user['completion_day_level']

        for day in range(1, 26):
            self.days.append(Problem(day, solves.get(str(day), None)))

    def build_stars(self):
        ls = [HEADER]
        ls.append(f"    {get_stars(self)}")
        return "```\n{}```".format("\n".join(ls))

    def build_averages(self):
        ttf_list = [x.part2_time for x in self.days if x.part2_time]
        if (len(ttf_list) == 0):
            debug(f"{self.name} has no completed days, skipping")
            return ("N/A", "N/A", "N/A")
        average_ttf = sum(ttf_list,datetime.timedelta()) / len(ttf_list)

        part_one_ttf_list = [x.part1_time for x in self.days if x.part1_time]
        part_one_ttf = sum(part_one_ttf_list,datetime.timedelta()) / len(part_one_ttf_list)
        
        part_two_ttf_list = [x.part2_time_delta for x in self.days if x.part2_time]
        part_two_ttf = sum(part_two_ttf_list,datetime.timedelta()) / len(part_two_ttf_list)
        
        return str(average_ttf).split(".")[0], str(part_one_ttf).split(".")[0], str(part_two_ttf).split(".")[0]

    def build_detailed_days(self):
        days = [x.breakdown for x in self.days]
        table = tabulate(days, headers=["Day","Part 1", "Part 2"])
        return "\n".join([x[1:] for x in table.split("\n")])

    def __repr__(self) -> str:
        return self.name
