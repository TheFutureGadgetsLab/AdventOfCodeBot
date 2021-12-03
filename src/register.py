import shelve
from logging import critical, debug, error, info, warning

import discord

from src.Leaderboard import Leaderboard
from src.utils import build_embed


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
                warning(f"user {username} attempted to register {author} but username not found")
                return "This user does not appear to be on the leaderboard."
        else:
            warning(f"user {username} attempted to register {author} but they are already registered")
            return "User already registered."
    info(f"user {username} registered as {author}")
    return f"{username} registered as {author}"

async def send_registered_users(ctx):
    debug("sending registered users")
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
