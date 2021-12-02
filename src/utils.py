import discord
import requests
import simplejson
from datetime import datetime
from src.config import YEAR, SESSION_COOKIE, URL


def truncate_name(name):
    return name[:18] + "…" if len(name) > 20 else name

def get_stars(player):
    string = []
    for day in range(0, 25):
        string.append(str(player.days[day]))
    return "".join(string) 

def build_embed(title, description, url, color, fields):
    embed=discord.Embed(
        title=title,
        description=description,
        url=url,
        color=color
    )
    for field in fields:
        embed.add_field(
            name = field[0], 
            value = field[1], 
            inline = field[2]
        )
    return embed

def build_leaderboard_embed(title: str, first_place: str, leaderboard):
    fields = [
        (f"{title} Leaderboard", leaderboard, False),
        ("\u200BGithub:", "https://github.com/bensonalec/AdventOfCodeBot", False)
    ]
    embed = build_embed(
        f"Advent of Code {YEAR}", 
        f"First place: {first_place}!", 
        "https://adventofcode.com", 
        discord.Color.red(), 
        fields
    )
    return embed

cached_response = None
cache_time = datetime.min

def query_leaderboard_API():
    #check the cachetime
    global cache_time
    global cached_response
    delta = datetime.now() - cache_time
    #check that it's been more than 15 minutes since the request has been tried
    if (delta.total_seconds() / 60) >= 15:
        print("Hitting API")
        cookies = dict(session=SESSION_COOKIE)
        response = requests.request("GET", URL, cookies=cookies)
        cache_time = datetime.now()
        cached_response = response.json()
    return cached_response

def check_validity_of_config():
    cookies = dict(session=SESSION_COOKIE)
    response = requests.request("GET", URL, cookies=cookies)
    if response.status_code == 404:
        print("Year is invalid.")
    if response.status_code == 500:
        print("Session cookie is invalid.")
    try:
        response.json()
    except simplejson.errors.JSONDecodeError: 
        print("JSON is malformed. This may be due to an invalid leadboard ID.")
        return False
    return response.status_code == 200