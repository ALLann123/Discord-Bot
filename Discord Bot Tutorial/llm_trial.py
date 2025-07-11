#!/usr/bin/python3
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from groq_llama import connect_llm

#load the environment variable files with API
load_dotenv()

#get the discord bot token
token=os.getenv("DISCORD_TOKEN")

handler=logging.FileHandler(filename='llm_discord.log', encoding='utf-8', mode='w')

#permissions the bot will do. Read the documentation
intents=discord.Intents.default()

intents.message_content=True
intents.members=True

#we can now call the bot using '!'
bot=commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def qwerty(ctx, *, msg):
    response = connect_llm(msg)

    # Discord message limit is 2000 characters
    for chunk in [response[i:i+2000] for i in range(0, len(response), 2000)]:
        await ctx.send(chunk)


#pass in our access token, log file and allow the debug to be written to the file
bot.run(token, log_handler=handler, log_level=logging.DEBUG)