## A Discord bot that broadcasts stats in your live League of Legends games

This bot allows members of a channel to register themselves by their League of Legends in-game name to be notified of opponents' ranks and win rates in any live games. The bot can be hosted on any device that supports Python and has a reliable internet connection. The code can also be stuck on a virtual machine in the cloud. For example, I currently host this on an AmazonEC2 Free Tier instance in AWS.


## Pre-requisites
The installation steps have been tested with Python3.8 on Ubuntu 18.04 and Amazon EC2 Linux. 

There are a number of ways to install Python3.8, but please note that certain dependencies may be missing when building from source. The following tutorials may be helpful for installing Python:
- [deadsnakes PPA](https://tooling.bennuttall.com/deadsnakes/) on Ubuntu
- [homebrew](https://docs.python-guide.org/starting/install3/osx/) on Mac OS X 

## Installation
Clone the repository and navigate into it

`git clone https://github.com/SamKnightGit/LeagueBot.git`

`cd LeagueBot`

Install pipenv if you do not already have it by following [the official docs](https://pipenv-fork.readthedocs.io/en/latest/install.html)

Install the project dependencies

`pipenv install`


## Adding secrets

In order to query the Riot API for game statistics you will need to acquire an API key: 

1. Navigate to the [Riot developer portal](https://developer.riotgames.com/) and sign up

2. On the main page you can generate a "Development API Key" but this will only be valid for 24 hours.

3. Click on `Register Product` on the main page and follow the process for a personal API key. Note that it may take a few days to be approved.

4. Once you have been approved you can find this API key by navigating to the `Apps` page

In order to respond to Discord messages you will also need a Discord bot token. This can be obtained by following the well-written [WriteBots guide](https://www.writebots.com/discord-bot-token/).

Once you have obtained both tokens you will need to add them to a file in the LeagueBot top-level directory called `secrets.py`. This file should have the following format:

```
RIOT_API_TOKEN = "<INSERT RIOT API TOKEN>"
DISCORD_BOT_TOKEN = "<INSERT DISCORD BOT TOKEN>"
```

**Note** that the values of these variables should be surrounded by quotation marks so they are interpreted as plain strings.


## Setting a dedicated channel
To set a channel which the bot will send messages to, you will need to find the channel ID. First enable developer mode:
1. Navigate to user settings (cog in the bottom left on Desktop application)
2. Click on `Advanced` under App Settings
3. Toggle on Developer Mode

You can now access the channel ID by right clicking on the relevant channel and selecting `Copy ID`

Finally, navigate to `main.py` and replace the value for STATS_CHANNEL_INDEX with your channel ID.
## Running the Bot

Activate the virtual environment to ensure you are using the correct dependency versions:

`pipenv shell`

Run the bot

`python3 main.py`


The following is an example of a bot message when a registered user enters a live game.
```
-----------------------------
-----------------------------
Sylas - <real summoner id>
Solo: GOLD IV 49.41% W/L
Flex: SILVER IV 45.61% W/L
-----------------------------
Caitlyn - <real summoner id>
Flex: SILVER II 41.38% W/L
Solo: SILVER I 43.75% W/L
-----------------------------
Gnar - <real summoner id>
Solo: GOLD III 54.79% W/L
Flex: GOLD III 66.67% W/L
-----------------------------
Neeko - <real summoner id>
Flex: SILVER II 47.13% W/L
Solo: GOLD IV 46.6% W/L
-----------------------------
Leona - <real summoner id>
Solo: GOLD II 50.11% W/L
-----------------------------
-----------------------------
```
&nbsp;

### Caveats
In the current implementation, all program state (context of registered users, associated games, etc.) is stored in memory. This means that exiting and re-running the program wipes out the record of registered users. With this in mind, I would recommend hosting in the cloud or on a low power device such as a Raspberry Pi.







