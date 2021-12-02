import shelve
import discord
from src.Leaderboard import Leaderboard
from src.config import YEAR
from src.utils import build_embed

async def run_stats(ctx, args):
    username = args
    player = None

    #asking for another players stats
    if username:
        with shelve.open('hachikuji.mayoi') as db:
            leaderboard = Leaderboard(db)
            player = next((pl for pl in leaderboard.players if pl.name.lower() == username), None)
    #asking for personal stats
    else:
        try:
            with shelve.open('hachikuji.mayoi') as db:
                myUser = db[str(ctx.author)]
                leaderboard = Leaderboard(db)
                player = [pl for pl in leaderboard.players if pl.name.lower() == myUser['username'].lower()][0]
        except KeyError:
            await ctx.message.channel.send("No user associated with your discord ID. Use `!register [AOC_USERNAME]` to associate")
            return
    if not player:
        await ctx.message.channel.send("User not found on your scoreboard.")
        return
    else:
        averages = player.build_averages()
        fields = [
            ("Stars", f"{player.stars} ⭐'s.\n{player.build_stars()}", False),
            ("Averages", f"Average time to finish each day: `{averages[0]}`\nAverage time to finish part one: `{averages[1]}`\nAverage time to finish part two: `{averages[2]}`", False),
            ("Details", f"```{player.build_detailed_days()[0:1023-6]}```", False),
            ("\u200BGithub:", "https://github.com/bensonalec/AdventOfCodeBot", False)
        ]
        embed = build_embed(f"Advent of Code {YEAR}", f"Individual stats for {player.name}!", "https://adventofcode.com", discord.Color.red(), fields)

        await ctx.message.channel.send(embed=embed)
