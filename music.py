import discord
import json

#import requests

from discord.ext import commands
from discord import FFmpegPCMAudio



token = ''#ADD YOUR BOT TOKEN HERE
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

queues = {}
badwords = ["bad", "gay"]

def check_queue(ctx, id):
    if queues[id] != []:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        player = voice.play(source)


@client.event
async def on_ready():
    print("Music BOT is ready")
    print("------------------")


@client.event
async def on_member_join(member):
    channel = client.get_channel(1150495382246264933)
    await channel.send(f"Welcome {member.mention}")


@client.event
async def on_member_remove(member):
    channel = client.get_channel(1150495382246264933)
    await channel.send("Goodbye " + str(member))



@client.command()
async def hello(ctx):
    await ctx.send("Hello")


@client.command(pass_context=True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('2Pac.mp3')
        player = voice.play(source)
    else:
        await ctx.send("Please Join A Voice Channel, Idiot.")


@client.command(pass_context=True)
async def stop(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("OK I'm leaving")
    else:
        await ctx.send("IDIOT! I'm not in a voice chat :angry:")


@client.command(pass_context=True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("There is no audio playing.")


@client.command(pass_context=True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("There is no song that is paused!")


@client.command(pass_context=True)
async def next(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)


@client.command(pass_context=True)
async def queue(ctx, arg):
    voice = ctx.guild.voice_client
    song = arg + '.mp3'
    source = FFmpegPCMAudio(song)

    guild_id = ctx.message.guild.id

    if guild_id in queues:
        queues[guild_id.append(source)]
    else:
        queues[guild_id] = [source]

    await ctx.send("'" + arg + "'" + " Added to queue")




@client.command()
async def gif(ctx, arg):

    # set the apikey and limit
    apikey = "AIzaSyCcely8nBJ7u6OEGT_xAze0KZnZceWcSA0"  # click to set to your apikey
    lmt = 1
    ckey = "my_test_app"  # set the client_key for the integration and use the same value for all API calls

    # our test search
    search_term = arg

    if arg not in badwords:
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



client.run(token)
