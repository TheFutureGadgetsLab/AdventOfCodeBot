import shelve
from discord.ext import commands
from asyncio import Lock
from src.Leaderboard import Leaderboard
from src.config import DISCORD_TOKEN, COMMAND_PREFIX
from src.utils import build_embed, build_leaderboard_embed, check_validity_of_config
from src.schedule import scheduler, run_schedule
from src.register import run_register
from src.start import run_start
from src.stats import run_stats
import discord
from logging import debug, info, warning, error, critical

bot = commands.Bot(command_prefix=COMMAND_PREFIX)
bot.remove_command('help')

data_mutex = Lock()

@bot.event
async def on_ready():
    info(f'logged in as {bot.user}')
    scheduler.remove_all_jobs()

@bot.command()
async def plb(ctx):
    debug(f'cmd> {ctx.author}: public leaderboard')
    with shelve.open('hachikuji.mayoi') as db:
        leaderboard = Leaderboard(db)
        await ctx.message.channel.send(
            embed=build_leaderboard_embed(
                "Public", 
                leaderboard.players_sorted_public()[0].name, 
                leaderboard.public_leaderboard()
            )
        )

@bot.command()
async def clb(ctx):
    debug(f'cmd> {ctx.author}: custom leaderboard')
    with shelve.open('hachikuji.mayoi') as db:
        leaderboard = Leaderboard(db)
        await ctx.message.channel.send(
            embed=build_leaderboard_embed(
                "Custom", 
                leaderboard.players_sorted_custom()[0].name, 
                leaderboard.custom_leaderboard()
            )
        )

@bot.command()
async def register(ctx, *arg):
    debug(f'cmd> {ctx.author}: register as {" ".join(arg)}')
    async with data_mutex:
        await run_register(ctx, " ".join(arg))

@bot.command()
async def start(ctx, arg):
    debug(f'cmd> {ctx.author}: start {arg}')
    async with data_mutex:
        msg = await run_start(ctx, arg)
    if msg:
        await ctx.message.channel.send(msg)

@bot.command()
async def schedule(ctx, *args):
    debug(f'cmd> {ctx.author}: schedule {" ".join(args)}')
    await run_schedule(ctx, " ".join(args))

@bot.command()
async def stats(ctx, *args):
    debug(f'cmd> {ctx.author}: stats {" ".join(args)}')
    await run_stats(ctx, " ".join(args).lower())

@bot.command()
async def help(ctx, *args):
    debug(f'cmd> {ctx.author}: help')
    await ctx.message.channel.send(
        embed =build_embed(
            "Advent of Code Bot Commands", 
            "", 
            "https://github.com/bensonalec/AdventOfCodeBot", 
            discord.Color.red(), 
            [
                (f"`{COMMAND_PREFIX}plb`", "Print out the private leaderboard. This uses the original advent of code scoring scheme.", False), 
                (f"`{COMMAND_PREFIX}clb`", "Prints out the custom leaderboard. This uses our custom advent of code scoring scheme.", False), 
                (f"`{COMMAND_PREFIX}register [AOC_USERNAME]`", "Associate yourself with given AoC user. Without argument will print out the list of registered users. With argument, will register your discord ID with your Advent of Code username for custom scoring.", False),
                (f"`{COMMAND_PREFIX}start <DAY_NUMBER>`", "Start a day. This will set your starttime for our custom scoring.", False),
                (f"`{COMMAND_PREFIX}schedule [<+/-><MINUTES>]`", "Can be called without an argument, if so will print the next scheduled send time. With an argument, will schedule a time for the leaderboard to send automatically. Takes in a indicator (either + or -) and an integer (minutes) and sends the leaderboard at the start time of the competition for that day (midnight EST), given that offset.", False),
                (f"`{COMMAND_PREFIX}stats [AOC_USERNAME]`", "Send individual stats for a user. Can be called with and without an argument, without an argument it will use the account that is registered with your user.", False),
            ]
        )
    )

if __name__ == "__main__":
    if check_validity_of_config():
        try:
            bot.run(DISCORD_TOKEN)
        except discord.errors.LoginFailure:
            error("invalid DISCORD_TOKEN!")
    else:
        error("invalid config file, see above for details")