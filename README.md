# Advent Of Code Discord Bot
![image](https://user-images.githubusercontent.com/9584084/141237987-6867c86d-58f5-4d1b-85be-f77bbc34a054.png)
Discord bot for displaying [Advent of Code](https://adventofcode.com) private leardboards, as well as custom leaderboards where participants can set their own start times. The latter function is ideal for participants in different time zones looking for a way to compete with each other.

## Table of Contents
- [Advent Of Code Discord Bot](#advent-of-code-discord-bot)
  - [Table of Contents](#table-of-contents)
  - [Screenshots](#screenshots)
  - [Getting Started](#getting-started)
  - [FAQ](#faq)
  - [Commands](#commands)
  - [Scoring](#scoring)
    - [Original Scoring](#original-scoring)
    - [Custom Scoring](#custom-scoring)
  - [Attribution](#attribution)

## Screenshots

| | |
|-|-|
| *The Leaderboard in Discord* | ![The !plb Command](https://media.Discordapp.net/attachments/732435214986510340/914383644288766012/unknown.png?width=418&height=300)
| *User Stats* | ![the !stats Command](https://media.Discordapp.net/attachments/732435214986510340/914385531528433704/unknown.png?width=324&height=678)

## Getting Started

1. `git clone https://github.com/TheFutureGadgetsLab/AdventOfCodeBot.git`. 
2. You'll need to [create a bot](https://discord.com/developers/docs/intro#bots-and-apps) in your Discord server for AdventOfCodeBot
3. You'll also need to enable the Message Content Intent for your bot.
4. Edit the config file located at `./src/config.py` with the following values:

| Value            | Description                                                                |
|------------------|----------------------------------------------------------------------------|
| `YEAR`           | Whichever year you are using for the leaderboard. Likely the current year. |
| `SESSION_COOKIE` | Session cookie you get when logging into Advent of Code. [(?)](https://github.com/wimglenn/advent-of-code-wim/issues/1)                    |
| `LEADERBOARD`    | ID of the private leaderboard you're trying to access. (it's in the leaderboard's URL)                             |
| `DISCORD_TOKEN`  | Token for the bot you created to be used by AdventofCodeBot. 

4. Install the dependencies `python3 -m pip install requirements`
5. `python3 main.py`     

## FAQ
aka questions that haven't been asked yet but probably will be
- **Why custom start times?**
    > We have a friend who lives in a timezone where Advent of Code problems release at 3:00AM, making it difficult for him to compete with us. With the bot anyone can start a problem when most convenient for them and have that time used in scoring.
- **Why is the scoreboard not updating right away?**
    > Advent of Code requests that the API only be accessed once every 15 minutes. We cache the previous API response for the leaderboard until 15 minutes have passed and then we update the cache.
- **Can I participate by registering my Discord ID with the leaderboard if I'm not actually on the Advent of Code private leaderboard?**
    > No, unfortunately not. You can only associate your Discord ID with a user found on the leaderboard. This is a neat idea though, and PRs are welcome.
- **What are these weird files called `hackikuji.mayoi` and `senjougahara.hitagi`?**
    > These are the shelve files that store state so it persists between bot shutdowns. `hackikuji.mayoi` stores the registered users and their start times, and `senjougahara.hitagi` stores the scheduled time for the server to run. Named after two characters from Monogatari.

## Commands
| Command                      | Description                                                                                                                                                                                                                                                                                                                                       |
|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `!plb`                       | Print out the private leaderboard. This uses the original Advent of Code scoring scheme.                                                                                                                                                                                                                                                          |
| `!clb`                       | Prints out the custom leaderboard. This uses our custom Advent of Code scoring scheme.                                                                                                                                                                                                                                                            |
| `!register [AOC_USERNAME]`   | When called without argument it will print all Discord users registered on the leaderboard. When called with argument (your name on the Advent of Code leaderboard), it will associate your Discord ID with that username.                                                                                                                            |
| `!start <DAY_NUMBER>`        | Start a day. This will set your starttime for our custom scoring.                                                                                                                                                                                                                                                                                 |
| `!schedule [<+/-><MINUTES>]` | Can be called without an argument, if so will print the next scheduled send time. With an argument, will schedule a time for the leaderboard to send automatically. Takes in a indicator (either + or -)  and an integer (minutes) and sends the leaderboard at the start time of the competition for that day (midnight EST), given that offset. |
| `!stats [AOC_USERNAME]`      | Send individual stats for a user. Can be called with and without an argument, without an argument it will use the account that is registered with your user.                                                                                                                                                                                      |          |

## Scoring
This bot provides two unique methods of scoring the leaderboard, specifically
based on start time of a problem. Both scoring methods follow the regular
Advent of Code scoring, but differ by which start time is used.

### Original Scoring
The original scoring (`!plb`) uses the exact same scoring conditions as the
original Advent of Code leaderboard, where start time for a problem is set by
the time the problem opens (Midnight EST) for each day. 

### Custom Scoring
The custom scoring (`!clb`) uses custom set start times by players.
These are set using the `!start <day>` command after a user has registered
with `!register <username>`. If a user has not set a start time for a problem,
the scoring algorithm will use the time that problem originally opened at
Midnight EST of that day.

## Attribution
Built by Future Gadgets Lab members
[@haydn-jones](https://github.com/haydn-jones),
[@bensonalec](https://github.com/bensonalec),
and [@benpm](https://github.com/benpm).
