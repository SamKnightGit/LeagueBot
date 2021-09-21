import time
import discord
import context
import secret
import asyncio
import league
import parse_data

STATS_CHANNEL_INDEX = 651818196751482880
client = discord.Client()
seconds_between_game_searches = 10
context_manager = context.ContextManager()
"""
Listens for any discord message sent to the bot:
    1)
    If message is "Register":
        User: "Register"
        Bot: "What is your league of legends ign?"
        User: "knightterror"
        Bot: "Found a match for user 'knightterror' is this correct? (y/n)"
        User: "y"
        Bot: "You have been registered!"

    2)
    If message is from a user which is already recognized by the bot:
        Hoclor: "Hi"
        AND game exists:
            Bot: "Here are stats for your current game Hoclor:"
        AND game does not exist:
            Bot: "I can't find your current game."

    3)
    If message is from user not registered with the bot:
        User: "Hi"
        Bot: "Sorry but I don't know who you are. Would you like to register? (y/n)"
        User: "y"
        GOTO 1
"""
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.type == discord.ChannelType.private:
        await context_manager.update_context(message.author.id, message)

"""
    Loop over all registered users:
    If user is in game:
        AND game has not already been added to list
            Add game ID to list
            Send opponent information to Discord channel
"""
async def search_for_games():
    while True:
        print("Searching for games")
        for user_id, user_context in context_manager.user_contexts.items():
            if user_context.is_registered:
                game_data = league.get_current_game(user_context.summoner_id)
                if game_data is None or game_data['gameId'] in context_manager.games.keys():
                    continue
                context_manager.add_game(game_data['gameId'])
                stats_channel = client.get_channel(STATS_CHANNEL_INDEX)
                stats = await parse_data.parse_game_data(game_data, user_context.summoner_id)
                print(stats)
                await stats_channel.send(stats)

        await asyncio.sleep(seconds_between_game_searches)


async def purge_games():
    while True:
        context_manager.purge_games()
        await asyncio.sleep(3600 * 24)

client.loop.create_task(purge_games())
client.loop.create_task(search_for_games())
client.run(secret.DISCORD_BOT_TOKEN)
