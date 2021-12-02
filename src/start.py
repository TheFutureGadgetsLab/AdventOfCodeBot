import shelve
from datetime import datetime
from logging import critical, debug, error, info, warning

from src.config import EST


async def run_start(ctx, arg):
    return start_session(arg, ctx.author)

def start_session(day, author):
    if(day.isnumeric()):
        with shelve.open('hachikuji.mayoi') as db:
            day = int(day) - 1
            if str(author) not in db:
                return "User not registered"
            a = db[str(author)]
            if a['start_times'][day] is None:
                a['start_times'][day] = datetime.now(tz=EST)
            else:
                return "Session already started."
            db[str(author)] = a
            return f"You ({db[str(author)]['username']}) started day {int(day) + 1}!"
    else:
        warning(f"invalid day {day}, day must be an integer")
        return "Day must be an integer."
