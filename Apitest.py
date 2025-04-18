import nextcord
from nextcord.ext import commands
import os
import wavelink

client = commands.Bot(command_prefix="!")
token = os.environ.get("") #ADD YOUR BOT TOKEN HERE


async def node_connect():
    await client.wait_until_ready()
    await wavelink.NodePool.create_node(bot=client, host='wavelinkonc.ml', port=443, password='incognito', https=True)

@client.event
async def on_ready():
    print("BOT is ready")
    client.loop.create_task(node_connect())

@client.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f"Node {node.identifier} is ready!")

@client.command()
async def play(ctx: commands.Context, *, search: str):
    if not ctx.author.voice or not ctx.author.voice.channel:
        return await ctx.send("You are not connected to any voice channel.")

    if not ctx.voice_client:
        vc = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    else:
        vc = ctx.voice_client

    if not vc.is_connected():
        return await ctx.send("I'm not connected to a voice channel.")

    tracks = await wavelink.NodePool.get_best_search_results(search, search_type=wavelink.YouTubeTrack)
    if not tracks:
        return await ctx.send("No tracks found.")

    if not vc.is_playing():
        await vc.play(tracks[0])
    else:
        await vc.queue.put(tracks[0])

client.run(token)