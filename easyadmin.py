import discord
import json
import os
from discord.app_commands import guild_only
from discord.ext import commands
from discord import Member, guild
from discord.ext.commands import has_permissions, MissingPermissions
import requests
import asyncio



intents = discord.Intents.default()
intents.typing = False
intents.members = True
intents.presences = False

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
token = "" #ADD YOUR BOT TOKEN HERE

profanity = ["fuck"]

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='FR ONG :('))
    print("EasyAdmin is Ready!")
    print("--------------------")

@client.event
async def on_member_join(member):
    channel = client.get_channel(1150495382246264933)
    await channel.send(f"Welcome {member.mention}")

@client.event
async def on_member_remove(member):
    channel = client.get_channel(1150495382246264)
    await channel.send(f"{member.mention} Just Left The Server")

@client.command()
async def hello(ctx):
    await ctx.send("Hello!")

@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"User {member} has been kicked")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You Don't Have Permission")

@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"User {member} has been banned")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You Don't Have Permission")

@client.command()
@has_permissions(administrator=True)
async def unban(ctx, member: discord.Member, *, reason=None):
    banned_users = await ctx.guild.bans()
    print(banned_users)
    member_name, member_discriminator = member.split("#")
    print(member_name)

    for ban_entry in banned_users:
        print(ban_entry)
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")
            return

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You Don't Have Permission")

@client.command()
async def embed(ctx):
    embed = discord.Embed(title="Dog", url="https://youtube.com", description="We love Dogs", colour=0xd94625)
    embed.set_author(name=ctx.author.display_name, url="https://www.instagram.com/moe_bruh1/", icon_url=ctx.author.avatar)
    embed.set_thumbnail(url="https://scontent.xx.fbcdn.net/v/t1.15752-9/377109737_636081555176493_7900894773123061385_n.jpg?stp=dst-jpg_p180x540&_nc_cat=107&ccb=1-7&_nc_sid=aee45a&_nc_ohc=4UOHTgHX3swAX94b9Br&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=03_AdTx1YdXFGGWYBA9LFgQlQorR3IUPEKOhOk8O156P8YPJQ&oe=65280A0A")

    embed.add_field(name="HEHE", value="Lobster", inline=True)
    embed.add_field(name="HAHA", value="Black", inline=True)
    embed.set_footer(text="Thank you retard")
    embed.set_image(url=ctx.author.avatar)

    await ctx.send(embed=embed)

@client.command()
async def avatar(ctx):
    embed = discord.Embed(title=f"Avatar of {ctx.author}", colour=0xd94625)
    embed.set_image(url=ctx.author.avatar)

    embed.add_field(name="REAL", value="Real")

    await ctx.send(embed=embed)


@client.command()
async def avatarof(ctx, member: discord.Member):
    embed = discord.Embed(title=f"Avatar of {member}", colour=0xd94625)
    embed.set_image(url=member.avatar.url)
    embed.add_field(name='', value='')

    await ctx.send(embed=embed)


@client.event
async def on_message(message):
    channel = client.get_channel(1150495382246264933)

    if message.author.id == 176752145700225024:
        if message.content.lower() == "w":
            await channel.send("STFU")

    await client.process_commands(message)



@client.command()
async def ea(ctx):
    await ctx.send("MAL MOK")


@client.command()
async def rtxt(ctx):
    path = "text.txt"
    embed = discord.Embed(title="File Content", colour=0xd94625)

    if os.path.exists(path):
        print("File Content: ")

    else:
        print("Doesnt exist")

    try:
        with open(path) as file:
            fil = file.read()
            embed.add_field(name="Read", value=(fil))
            await ctx.send(embed=embed)
            #await ctx.send("\n"+(file.read())+"\n")
    except FileNotFoundError:
        await ctx.send("File was not Found")

@client.command()
async def wtxt(ctx, *message):
    try:
        with open('text.txt', 'w') as file:
            file.write(' '.join((message)))
            await ctx.send("File Written Successfully")

    except FileNotFoundError:
        await ctx.send("File was not Found")
    await client.process_commands(message)

@client.command()
async def gif(ctx, arg):
    # set the apikey and limit
    apikey = ""  # click to set to your apikey
    lmt = 1
    ckey = "my_test_app"  # set the client_key for the integration and use the same value for all API calls

    # our test search
    search_term = arg

    if arg not in profanity:
        # get the top 8 GIFs for the search term
        r = requests.get(
            "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (search_term, apikey, ckey, lmt))
        channel = client.get_channel(1150162723104104502)
        if r.status_code == 200:
            # load the GIFs using the urls for the smaller GIF sizes
            top_8gifs = json.loads(r.content)
            print(top_8gifs)
        else:
            top_8gifs = None
        if top_8gifs:
            message = f"Here are some GIFs related to '{arg}':\n"
            for gif in top_8gifs['results']:
                message += f"{gif['itemurl']}\n"

            # Split the message into smaller chunks if it's too long
            message_chunks = [message[i:i + 2000] for i in range(0, len(message), 2000)]

            for chunk in message_chunks:
                await ctx.send(chunk)
        else:
            await ctx.send("No GIFs found.")
    else:
        await ctx.channel.send("WARNING")


class Map:
    def __init__(self):
        # Initialize map-related properties or components here
        self.iss_marker = None
        self.isscirc_marker = None

    def set_location(self, lat, lon):
        # Update the ISS marker and circle on the map
        # This is just a placeholder; you need to implement this based on your actual map implementation
        print(f"Updating map with ISS location: Lat {lat}, Lon {lon}")
map_instance = Map()

@client.command()
async def iss(ctx):
    url = 'http://api.open-notify.org/iss-now.json'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        lat = data['iss_position']['latitude']
        lon = data['iss_position']['longitude']

        # Update the map with the ISS location
        map_instance.set_location(lat, lon)

        await ctx.send(f"ISS is currently at latitude {lat} and longitude {lon}.")
    else:
        await ctx.send("Failed to fetch ISS location.")

    #await asyncio.sleep(5)
    #await iss(ctx)


@client.command()
async def snd(ctx, user: discord.Member, *, msg):
    user = ctx.message.server.get_member(user)
    await client.send(user, msg)

@client.command(pass_context=True)
async def dm(ctx, member: discord.Member, arg, message=None):
    message = arg
    await member.send(message)


client.run(token)

