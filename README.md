# Advent Of Code Discord Bot
![image](https://user-images.githubusercontent.com/9584084/141237987-6867c86d-58f5-4d1b-85be-f77bbc34a054.png)
Discord bot for displaying [Advent of Code](https://adventofcode.com) private leardboards, as well as custom leaderboards where participants can set their own start times. The latter function is ideal for participants in different time zones looking for a way to compete with each other.

## Screenshots

*The Leaderboard in Discord*

![The !plb Command](https://media.discordapp.net/attachments/732435214986510340/914383644288766012/unknown.png?width=944&height=678)

*User Stats*

![the !stats Command](https://media.discordapp.net/attachments/732435214986510340/914385531528433704/unknown.png?width=324&height=678)

## Commands
| Command                      | Description                                                                                                                                                                                                                                                                                                                                       |
|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `!plb`                       | Print out the private leaderboard. This uses the original advent of code scoring scheme.                                                                                                                                                                                                                                                          |
| `!clb`                       | Prints out the custom leaderboard. This uses our custom advent of code scoring scheme.                                                                                                                                                                                                                                                            |
| `!register [AOC_USERNAME]`   | Associate yourself with given AoC user. Can be called without an argument, if so will print out the list of registered users. If no argument, will register your discord ID with your Advent of Code username for custom scoring.                                                                                                                 |
| `!start <DAY_NUMBER>`        | Start a day. This will set your starttime for our custom scoring.                                                                                                                                                                                                                                                                                 |
| `!schedule [<+/-><MINUTES>]` | Can be called without an argument, if so will print the next scheduled send time. With an argument, will schedule a time for the leaderboard to send automatically. Takes in a indicator (either + or -)  and an integer (minutes) and sends the leaderboard at the start time of the competition for that day (midnight EST), given that offset. |
| `!stats [AOC_USERNAME]`      | Send individual stats for a user. Can be called with and without an argument, without an argument it will use the account that is registered with your user.                                                                                                                                                                                      |

## Running the bot
1. Clone this repo to your machine with `git clone https://github.com/TheFutureGadgetsLab/AdventOfCodeBot.git`. 
2. Run `python3 -m pip install requirements`
3. Run `python3 main.py`

## Getting Started
To get started, you will need to create a bot in your discord server for AdventOfCodeBot, then fill in the config located at `./src/config.py` with the following values:

| Value            | Description                                                                |
|------------------|----------------------------------------------------------------------------|
| `YEAR`           | Whichever year you are using for the leaderboard. Likely the current year. |
| `SESSION_COOKIE` | Session cookie you get when logging into Advent of Code.                   |
| `LEADERBOARD`    | ID of the leaderboard you're trying to access.                             |
| `DISCORD_TOKEN`  | Token for the bot you created to be used by AdventofCodeBot.               |

## Scoring
This bot provides two unique methods of scoring the leaderboard, specifically based on start time of a problem. Both scoring methods work by counting the number of players on the leaderboard (n), then for each star giving the first player to finish n stars, the second player n - 1 stars, and so on, until the last player recieves 1 star. 

### Original Scoring
The original scoring (`!plb`) uses the exact same scoring conditions as the original advent of code leaderboard, where start time for a problem is set by the time the problem opens (Midnight EST) for each day. 

### Custom Scoring
The custom scoring (`!clb`) uses custom set start times by players. These are set using the `!start <day>` command after a user has registered with `!register <username>`. If a user has not set a start time for a problem, the scoring algorithm will use the time that problem originally opened at Midnight EST of that day.

### FAQ
1. What are these weird files called `hackikuji.mayoi` and `senjougahara.hitagi`?  
These are the shelve files that store state so it persists between bot shutdowns. hackikuji.mayoi stores the registered users and their start times, and senjougahara.hitagi stores the scheduled time for the server to run.

## Attribution
Built by Future Gadgets Lab members [@haydn-jones](https://github.com/haydn-jones), [@bensonalec](https://github.com/bensonalec), and [@benpm](https://github.com/benpm).
