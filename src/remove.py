import shelve
from logging import critical, debug, error, info, warning


async def run_remove(ctx,arg):
    return remove_session(arg, ctx.author)

def remove_session(day, author):
    if(day.isnumeric()):
        with shelve.open('hachikuji.mayoi') as db:
            day = int(day) - 1
            if str(author) not in db:
                return "User not registered"
            a = db[str(author)]
            if a['start_times'][day] is None:
                return "No session started."
            else:
                a['start_times'][day] = None
            db[str(author)] = a
            return f"You ({db[str(author)]['username']}) removed your start time for day {int(day) + 1}!"
    else:
        warning(f"invalid day {day}, day must be an integer")
        return "Day must be an integer."
