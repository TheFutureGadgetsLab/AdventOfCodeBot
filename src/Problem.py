from typing import Optional
from datetime import datetime

from src.config import YEAR, UTC, EST

class Problem:
    def __init__(self, day: int, problem: dict):
        self.day = day
        self.parts_finished = 0
        self.start_time = None
        self.part1_finish_time = None
        self.part2_finish_time = None
        self.parse_dict(problem)

    def parse_dict(self, problem: Optional[dict]):
        self.start_time = datetime(year=YEAR, month=12, day=self.day, hour=0, tzinfo=EST)
        if problem:
            self.part1_finish_time = datetime.fromtimestamp(problem['1']['get_star_ts'], tz=UTC)
            self.parts_finished = 1
            if '2' in problem:
                self.part2_finish_time = datetime.fromtimestamp(problem['2']['get_star_ts'], tz=UTC)
                self.parts_finished = 2

    @property
    def part1_time(self):
        if self.part1_finish_time:
            return self.part1_finish_time - self.start_time
        return None
    
    @property
    def part2_time(self):
        if self.part2_finish_time:
            return self.part2_finish_time - self.start_time
        return None

    @property
    def part2_time_delta(self):
        if self.part2_finish_time:
            return self.part2_finish_time - self.part1_finish_time
        return None

    @property
    def breakdown(self):
        toSend = [str(self.day)]
        if self.part1_time:
            toSend.append(str(self.part1_time))
        if self.part2_time:
            toSend.append(str(self.part2_time_delta))
        return toSend

    def __str__(self) -> str:
        return [" ", "-", "+"][self.parts_finished]
    
