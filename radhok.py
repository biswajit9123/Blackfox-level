import discord
from discord.ext import commands
import os
import random
import json
import asyncio
import colorsys
import time

client = commands.Bot(description="Blackfox Official Bot", command_prefix=commands.when_mentioned_or("^"), pm_help = True)
client.remove_command('help')

#show when it connects to discord
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)

@client.event
async def on_message(message):
    user_add_xp(message.author.id, 2)
    await client.process_commands(message)
    if message.content.lower().startswith('^dailyrank'):
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        level=int(get_xp(message.author.id)/100)
        msgs=int(get_xp(message.author.id)/2)
        embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_author(name='Daily Universal Rank')
        embed.set_thumbnail(url = message.author.avatar_url)
        embed.add_field(name = '**__XP__**'.format(message.author),value ='``{}``'.format(get_xp(message.author.id)),inline = False)
        embed.add_field(name = '**__Level__**'.format(message.author),value ='``{}``'.format(level),inline = False)
        embed.add_field(name = '**__Messages__**'.format(message.author),value ='``{}`` Messages'.format(msgs),inline = False)
        embed.add_field(name='Note:',value='Our bot reset all ranks everyday so it shows only daily rank')
        await client.send_message(message.channel, embed=embed)
     
def user_add_xp(user_id: int, xp: int):
    if os.path.isfile("users.json"):
        try:
            with open('users.json', 'r') as fp:
                users = json.load(fp)
            users[user_id]['xp'] += xp
            with open('users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)
        except KeyError:
            with open('users.json', 'r') as fp:
                users = json.load(fp)
            users[user_id] = {}
            users[user_id]['xp'] = xp
            with open('users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)
    else:
        users = {user_id: {}}
        users[user_id]['xp'] = xp
        with open('users.json', 'w') as fp:
            json.dump(users, fp, sort_keys=True, indent=4)


def get_xp(user_id: int):
    if os.path.isfile('users.json'):
        with open('users.json', 'r') as fp:
            users = json.load(fp)
        return users[user_id]['xp']
    else:
        return 0

@client.event
async def on_reaction_add(reaction, user):
    if reaction.emoji == "🇻":
        role = discord.utils.get(reaction.message.server.roles, name="Verified")
        await client.add_roles(user, role)
        await client.send_message(user, f'Added Verified role in {reaction.message.server}')

@client.event
async def on_reaction_remove(reaction, user):
    if reaction.emoji == "🇻":
        role = discord.utils.get(user.server.roles, name="Verified")
        await client.remove_roles(user, role)
        await client.send_message(user, f'Removed Verified role in {reaction.message.server}')
        
@client.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def setreactionverify(ctx):
    author = ctx.message.author
    server = ctx.message.server
    everyone_perms = discord.PermissionOverwrite(send_messages=False,read_messages=True)
    everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
    await client.create_channel(server, '★verify-for-chatting★',everyone)
    for channel in author.server.channels:
        if channel.name == '★verify-for-chatting★':
            react_message = await client.send_message(channel, 'React with 🇻 to Verify | Sometimes it not works so you can also use mv!verify anywhere(Where you can send messages)')
            reaction = '🇻'
            await client.add_reaction(react_message, reaction)
  

client.run(os.getenv('Token'))
