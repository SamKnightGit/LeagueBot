import discord


async def base(message):
    await message.channel.send("")


async def game_not_found(message):
    await message.channel.send("I could not find the game you are currently in.")


async def game_data(message, game_data):
    await message.channel.send("Found the current game: ")


async def league_ign_prompt(message):
    await message.channel.send("What is your league of legends ign?")


async def league_ign_not_found(message):
    await message.channel.send("Sorry but I could not find your summoner name on EUW.")


async def league_ign_confirm(message):
    await message.channel.send(f"Found a match for user '{message.content}' is this correct? (y/n)")


async def register_successful(message):
    await message.channel.send("You have been registered successfully!")


async def register_prompt(message):
    await message.channel.send("Sorry but I don't know who you are. Would you like to register? (y/n)")


async def cancel_operation(message):
    await message.channel.send("Ok resetting...")


async def deregister_prompt(message):
    await message.channel.send("Are you sure you want to deregister (y/n)?")


async def deregister_successful(message):
    await message.channel.send("You have been deregistered.")
