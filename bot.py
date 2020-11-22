import os
import random
import requests
from collections.abc import Sequence
import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

import logging

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
ION_API_URL = os.getenv('ION_API_URL')
ION_USER = os.getenv('ION_USER')
ION_PASS = os.getenv('ION_PASS')
ADMIN_ROLE = os.getenv('ADMIN_ROLE')
STUDENT_ROLE = os.getenv('STUDENT_ROLE')


ROLES = [
    'Aileen Rashid',
    'Alan Jiang',
    'Alex Yung',
    'Allen Huo',
    'Ally Estabillo',
    'Amy Wang',
    'Anisha Talreja',
    'Ann Shen',
    'Archi Patel',
    'Arnav Kadam',
    'Benoy Sen',
    'Bradley Cao',
    'Caroline Xu',
    'Charu Mehta',
    'Christina Han',
    'Cindy Yang',
    'Daniel Kim',
    'Daniel Shi',
    'Danniel Cao',
    'Dhanbee Suh',
    'Elina Liu',
    'Elisabeth Everhart',
    'Elise Zhu',
    'Ellie Chen',
    'Elliott Lee',
    'Bryan Hong',
    'Emma Cox',
    'Estan Rodriguez',
    'Evelyne Breed',
    'Harini Ramaswamy',
    'Harshil Koyyalamudy',
    'Helen Fu',
    'Isabella Zhu',
    'Jason Lee',
    'Jay Varakala',
    'Jayant Kammula',
    'Jeffery Lin',
    'Jeffrey Chen',
    'Jeremy Kim',
    'Jessica Chung',
    'Jessica Wang',
    'Johanna Lohmus',
    'Jonathan Buchholz',
    'Jordan Lee',
    'Jorge Duggar',
    'Katelyn Chen',
    'Kisna Matta',
    'Kritika Kumar',
    'Leah Connell',
    'Margaret Gao',
    'Matthew Kim',
    'Matthew Li',
    'Maxx Yang',
    'Myles Bao',
    'Nathaniel Kenschaft',
    'Neil Agrawal',
    'Nihal Shah',
    'Niyathi Vadlapatla',
    'Noah Cha',
    'Praneeth Bhandaru',
    'Michael Sun',
    'Raheel Shaik',
    'Richard Xu',
    'Rohan Kompella',
    'Ronel Sahoo',
    'Rushil Umaretiya',
    'Samuel Gwon',
    'Sameer Gabbita',
    'Samuel Turner',
    'Sashvad Satish Kumar',
    'Satvik Matta',
    'Sherry Yu',
    'Shivank Bhimavarapu',
    'Simrith Ranjan',
    'Sophie King',
    'Srishty Muthusekaran',
    'Sumanth Moole',
    'Suraj Vaddi',
    'Tanishk Govil',
    'Tanmai Kalisipudi',
    'Tarini Basireddy',
    'Tianhao Chen',
    'Tyler Richard',
    'Vani Gupta',
    'Vinay Ayala',
    'Vivian Gao',
    'Yulee Kang',
    'Amruta Rajeev',
    'Arnav Jain',
    'Aryan Rajput',
    'Clarissa Ding',
    'Grace Guan',
    'Emily Cui',
    'Alex Li',
    'Vishal Kotha',
    'Irene Ko',
    'Jessica May',
    'Kavyesh Pasham',
    'Krisha Pahwa',
    'Lillani Horcharoen',
    'Patrick Gaucher',
    'Aidan Ludwig',
    'Anish Susarla',
    'Rushil Umaretiya',
    'Tiffany Lee',
    'Sahishnu Hanumansetty',
    'Victoria Wang',
    'Wilson Chen',
    'Deccan Maniam',
]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    guild = await bot.fetch_guild(GUILD)
    print(f'Logged in as {bot.user.name} on {guild}')

def make_sequence(seq):
    if seq is None:
        return ()
    if isinstance(seq, Sequence) and not isinstance(seq, str):
        return seq
    else:
        return (seq,)

def message_check(channel=None, author=None, content=None, ignore_bot=True, lower=True):
    channel = make_sequence(channel)
    author = make_sequence(author)
    content = make_sequence(content)
    if lower:
        content = tuple(c.lower() for c in content)
    def check(message):
        if ignore_bot and message.author.bot:
            return False
        if channel and message.channel not in channel:
            return False
        if author and message.author not in author:
            return False
        actual_content = message.content.lower() if lower else message.content
        if content and actual_content not in content:
            return False
        return True
    return check

@bot.event
async def on_member_join(member):

    await member.create_dm()
    await member.dm_channel.send(
        f'Hey {member.name}, you\'re almost ready to get into the action! Just reply to me with your `Ion` username (e.g. 2023sstern) and I\'ll verify you!'
    )
    verify = False
    attempts = 5
    while not verify and attempts > 0:
        attempts -= 1
        
        reply = await bot.wait_for("message", check=message_check(channel=member.dm_channel))
        print ('reply: ' + reply.content)
        try:
            response = requests.get(ION_API_URL+f'/profile/{reply.content}', auth=requests.auth.HTTPBasicAuth(ION_USER, ION_PASS)).json()
            nick = response['full_name']
            grade = response['grade']['name']
            first_name = response['first_name']
        except:
            response, nick, first_name = None, None, None

        if nick != None:
            if grade == 'sophomore':
                guild = await bot.fetch_guild(GUILD)
                role = get(guild.roles, name="Student")
                await member.add_roles(role)
                await member.edit(nick=nick)
                await member.dm_channel.send(
                    f'Good stuff :sparkles:{member.mention}:sparkles:, you just got the Student role on the TJ 2023 discord server, and you should be able to access all the channels!'
                    f'```don\'t go too wild```'
                )
                break
            else:
                await member.dm_channel.send(
                    f'Woah there buckaroo, this server is for 2023 gang only. Watch it.'
                )
        await member.dm_channel.send(
            f'Sorry, but that didn\'t work, please just put your Ion username and nothing else (e.g. `2023sstern`)'
            f'You have {attempts} attempts remaining.'
        )
    else:
        await member.dm_channel.send(
            f'Bummer dude, but don\'t worry, just DM any of the Class 🅱️ouncil (@Rushilwiz#4303) and they\'ll get it fixed for u ;)'
        ) 

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

@bot.command(name='schedule', help='Gets schedule off Ion')
async def schedule(ctx):
    schedule = requests.get(ION_API_URL+'/schedule', auth=requests.auth.HTTPBasicAuth(ION_USER, ION_PASS)).json()
    try:
        # await ctx.send('\n'.join([f"{i['name']} {i['start']}-{i['end']}" for i in schedule['results'][0]['day_type']['blocks']]))

        title = remove_html_tags(schedule['results'][0]['day_type']['name'])
        if 'blue' in title.lower():
            embed = discord.Embed(title=remove_html_tags(schedule['results'][0]['day_type']['name']), color=0x779ecb) #,color=Hex code , color='ff0000'
        elif 'red' in title.lower():
            embed = discord.Embed(title=remove_html_tags(schedule['results'][0]['day_type']['name']), color=0xff0000)
        embed.add_field(name="Blocks:", value='\n'.join([f"{i['name']} {i['start']}-{i['end']}" for i in schedule['results'][0]['day_type']['blocks']]))
        message = await ctx.send(embed=embed)
        for emoji in ('🇮', '🇴', '🇳'):
            await message.add_reaction(emoji)
    except:
        await ctx.send('ayo sorry dawg I couldn\'t fetch the schedule')

@bot.command(name='announcements', help='Gets announcements off Ion')
async def schedule(ctx):
    announcements = requests.get(ION_API_URL+'/announcements', auth=requests.auth.HTTPBasicAuth(ION_USER, ION_PASS)).json()
    #try:
    embed = discord.Embed(title="Announcements:", url="https://ion.tjhsst.edu/")
    for announcement in announcements['results'][:5]:
        embed.add_field(name=remove_html_tags(announcement['title']), value=remove_html_tags(announcement['content'])[:500]+'...', inline=False)
    message = await ctx.send(embed=embed)
    for emoji in ('🇮', '🇴', '🇳'):
        await message.add_reaction(emoji)


@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

@bot.command(name='info', help='Gets profile info for a user on Ion')
@commands.has_role(ADMIN_ROLE)
async def info(ctx, username):
    info = requests.get(ION_API_URL+f'/profile/{username}', auth=requests.auth.HTTPBasicAuth(ION_USER, ION_PASS)).json()
    await ctx.send('\n'.join([f"{i}: {info[i]}" for i in info]))
    for emoji in ('🇮', '🇴', '🇳'):
        await message.add_reaction(emoji)

@bot.command(name='ping')
async def ping(ctx) :
    await ctx.send(f":ping_pong: Pong    `Latency: {format(round(bot.latency * 1000, 1))}ms`")

@bot.command(name="whoami")
@commands.has_role(ADMIN_ROLE)
async def whoami(ctx) :
    await ctx.send(f"You are {ctx.message.author.name}")

@bot.command(name='purge')
@commands.has_role(ADMIN_ROLE)
async def clear(ctx, amount=5) :
    await ctx.channel.purge(limit=amount+1)

@bot.command(name='clear')
@commands.has_role(ADMIN_ROLE)
async def clear(ctx, amount=5) :
    await ctx.channel.purge(limit=amount)

@bot.command(name='clear_channel')
@commands.has_role(ADMIN_ROLE)
async def clear_channel(ctx):

    await ctx.send("aight listen this will remove ***EVERYTHING*** in this channel, reply `Yes` (within the next 5s) if you really want to do this.")
    def check(m):
        return m.content.lower() == "yes"

    try:
        msg = await bot.wait_for("message", check=check, timeout=5.0)
    except:
        await ctx.send("ok, I'm not doing it.")
    else:
        await ctx.send("Your funeral!")
        await ctx.channel.purge()

@bot.command(name='purge_channel')
@commands.has_role(ADMIN_ROLE)
async def purge_channel(ctx):

    await ctx.send("aight listen this will remove ***EVERYTHING*** in this channel, reply `Yes` (within the next 5s) if you really want to do this.")
    def check(m):
        return m.content.lower() == "yes"

    try:
        msg = await bot.wait_for("message", check=check, timeout=5.0)
    except:
        await ctx.send("ok, I'm not doing it.")
    else:
        await ctx.send("Your funeral!")
        for i in range(5):
            await ctx.channel.purge(limit=999)

@bot.command(name='members')
@commands.has_role(ADMIN_ROLE)
async def get_members(ctx):
    for guild in bot.guilds:
        if guild.name == 'TJ 2023':
            break
        
    members = '\n - '.join([member.name for member in guild.members])
    await ctx.send(f'Guild Members:\n - {members}\n Total: {len(guild.members)}')

@bot.command(name='nicknames')
@commands.has_role(ADMIN_ROLE)
async def get_members(ctx):
    guild = ctx.guild
    members = '\n'.join([member.display_name for member in guild.members])
    await ctx.send(f'Guild Members:\n{members}\n Total: {len(members)}')



@bot.command(name='create-roles')
@commands.has_role(ADMIN_ROLE)
async def get_members(ctx):
    guild = ctx.guild
    for name in ROLES:
        print(name)
        await guild.create_role(name=name)


@bot.event
async def on_command_error(ctx, error):
    
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You don\'t have the correct permissions for this command. :billed_cap:.')
@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            f.write(f'Other error: {args[0]}\n')

bot.run(TOKEN)