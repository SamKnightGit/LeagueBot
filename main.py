import time
import discord
import context
import secret
client = discord.Client()
time_between_game_searches = 10
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

    await context_manager.update_context(message.author.id, message)

"""
    Loop over all registered users:
    If user is in game:
        AND game has not already been added to list
            Add game ID to list
            Send opponent information to slack channel
"""
def search_for_games():
    pass


client.run(secret.DISCORD_BOT_TOKEN)
# while True:
#     search_for_games()
#     time.sleep(time_between_game_searches)