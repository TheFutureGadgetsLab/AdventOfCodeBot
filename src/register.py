import shelve
import discord
from src.utils import build_embed
from src.Leaderboard import Leaderboard

async def run_register(ctx, arg):
    if arg:
        msg = register_user(arg, ctx.author)
        if msg:
            await ctx.message.channel.send(msg)
    else:
        await send_registered_users(ctx)

def register_user(username, author):
    with shelve.open('hachikuji.mayoi') as db:
        leaderboard = Leaderboard(db)
        players = [x.name.lower() for x in leaderboard.players]
        if str(author) not in db:
            if username.lower() in players:
                db[str(author)] = {
                    'start_times': {k:None for k in range(0,25)},
                    'username': username
                }
            else:
                return "This user does not appear to be on the leaderboard."
        else:
            return "User already registered."
    return f"{username} registered as {author}"

async def send_registered_users(ctx):
    fields = []
    with shelve.open('hachikuji.mayoi') as db:
        for key, value in db.items():
            fields.append((key, value['username'], True))
    embed = build_embed(
        "Registered Users", 
        "The list of users who have registered their Discord ID with an Advent of Code username.",
        "https://github.com/bensonalec/AdventOfCodeBot",
        discord.Color.red(),
        fields
    )
    await ctx.message.channel.send(embed=embed)
