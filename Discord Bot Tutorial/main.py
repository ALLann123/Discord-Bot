#!/usr/bin/python3
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os


#load the environment variable files with API
load_dotenv()

#get the discord bot token
token=os.getenv("DISCORD_TOKEN")

handler=logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

#permissions the bot will do. Read the documentation
intents=discord.Intents.default()

intents.message_content=True
intents.members=True

#we can now call the bot using '!'
bot=commands.Bot(command_prefix='!', intents=intents)

secret_role="fScociety"

#we use the python decorator, and get the events to trigger the bot
@bot.event
async def on_read():
    print("We are ready to go in, {bot.user.name}")

#sends private message to a member when they join
@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")

@bot.event
async def on_message(message):
    #prevent the bot from replying to its own message
    if message.author==bot.user:
        return

    #remove message with bad message
    if "shit" in message.content.lower():
        #delete the message
        await message.delete()
        #tag the author of the message
        await message.channel.send(f"{message.author.mention}- dont use that word")

    #allows bot continues processing the rest of the messages. Make sure we have all of this
    await bot.process_commands(message)
        
#sometimes we want to talk directly to the bot
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}")

#assigning Roles to someone
@bot.command()
async def assign(ctx):
    role=discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {secret_role}")
    
    else:
        await ctx.send("Role Doesnt exist")

#now lets give bot the ability to remove a role
@bot.command()
async def remove(ctx):
    role=discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {secret_role} removed")
    else:
        await ctx.send("Role Doesnt exist")

#how to send a direct message to someone
@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said {msg}")

#directly replying to the message
@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your message")


#the one calling this command should have been assigned the role
@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send("Welcome to the club!")

#exception handling of any of the above having an error
@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to do that!")

@bot.command()
async def poll(ctx, *, question):
    embed=discord.Embed(title="New Poll", description=question)
    poll_message=await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

#pass in our access token, log file and allow the debug to be written to the file
bot.run(token, log_handler=handler, log_level=logging.DEBUG)



