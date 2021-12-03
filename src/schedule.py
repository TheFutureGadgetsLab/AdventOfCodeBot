import shelve
from datetime import datetime
from logging import critical, debug, error, info, warning

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from src.config import EST
from src.Leaderboard import Leaderboard
from src.utils import build_leaderboard_embed

scheduler = AsyncIOScheduler()
scheduler.start()

async def run_schedule(ctx, arg):
    if not arg:
        #send the next scheduled send time
        try:
            with shelve.open('senjougahara.hitagi') as db:
                hours, minutes = db["scoreboard_send_time"]
                await ctx.message.channel.send(f"The next scheduled scoreboard will send at {hours}:{minutes} EST.")
        except KeyError:
            warning("no scheduled scoreboard send time found")
            await ctx.message.channel.send("There is no scheduled next time to send.")
        return

    if len(arg) < 2:
        warning(f"invalid schedule input '{arg}'")
        await ctx.message.channel.send("Invalid input. Usage: !schedule +/-offset (where offset is time before (-) or after (+) open).")
        return

    indicator = arg[0]
    offset = arg[1:]
    #check that the input is valid
    if not(indicator in ["-", "+"] and offset.isnumeric()):
        warning(f"invalid schedule input '{arg}'")
        await ctx.message.channel.send("Invalid input. Usage: !schedule +/-offset (where offset is time before (-) or after (+) open).")
        return

    #store that offset
    if indicator == "-":
        minutes = - int(offset)
    else:
        minutes = int(offset)

    hours =  24 - (abs(minutes // 60)) if indicator == "-" else abs(minutes) // 60
    minutes = minutes % 60
    print(hours, minutes)
    with shelve.open('senjougahara.hitagi') as db:
        db["scoreboard_send_time"] = (hours, minutes)

    #initializing scheduler
    await schedule_job(ctx)

async def schedule_job(ctx):
    with shelve.open('senjougahara.hitagi') as db:
        hours, minutes = db["scoreboard_send_time"]
    scheduler.remove_all_jobs()
    if datetime.now().month >= 11:
        scheduler.add_job(
            send_scheduled_message, 
            CronTrigger(
                hour=str(hours), 
                minute=str(minutes), 
                second="0", 
                timezone=EST
            ), 
            args=[ctx]
        ) 
        await ctx.message.channel.send(f"Successfully added scheduled time! The next scheduled scoreboard will send at {hours}:{minutes} EST.")
    else:
        warning("No longer scheduling scoreboard messages, as it is not November or December")
        ctx.message.channel.send("No longer scheduling scoreboard messages, as it is not November or December.")

async def send_scheduled_message(ctx):
    with shelve.open('hachikuji.mayoi') as db:
        leaderboard = Leaderboard(db)
        await ctx.message.channel.send(
            embed=build_leaderboard_embed(
                "Custom", 
                leaderboard.players[0].name, 
                leaderboard.custom_leaderboard()
            )
        )
    await schedule_job(ctx)
