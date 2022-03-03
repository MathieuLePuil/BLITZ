import asyncio
import json
import random

import DiscordUtils
import discord
import youtube_dl
from discord.ext import commands
from discord_slash import SlashCommand


async def get_prefix(message):
    with open("/home/mmi21b12/DISCORD/BLITZ/prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


bot = commands.Bot(command_prefix=get_prefix)
musics = {}
ytdl = youtube_dl.YoutubeDL()
music = DiscordUtils.Music()
bot.remove_command("help")
slash = SlashCommand(bot, sync_commands=True)

extensions = ['prefix']


# py Desktop\Bots_Discord\Blitz\main.py


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name=f"sur {len(bot.guilds)} serveurs | *help"))
    await bot.change_presence(activity=discord.Game(f"être codé par Dr3Xt3r"))
    await bot.change_presence(activity=discord.Game(f"BOT de Musique"))

    print("Blitz est démarré")


async def ch_pr():
    await bot.wait_until_ready()

    statuses = [f"sur {len(bot.guilds)} serveurs | *help", "être codé par Dr3Xt3r", "BOT Musique"]

    while not bot.is_closed():
        status = random.choice(statuses)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))

        await asyncio.sleep(10)


bot.loop.create_task(ch_pr())


@bot.command()
async def join(ctx):
    voicetrue = ctx.author.voice
    if voicetrue is None:
        return await ctx.send("**Blitz** ne peut pas se connecter car vous n'êtes pas dans un salon vocal !")
    await ctx.author.voice.channel.connect()
    await ctx.send("**Blitz** a rejoint votre *salon vocal* !")


@bot.command()
async def leave(ctx):
    voicetrue = ctx.author.voice
    mevoicetrue = ctx.guild.me.voice
    if voicetrue is None:
        return await ctx.send("**Blitz** ne peut pas se déconnecter car vous n'êtes pas dans le salon vocal !")
    if mevoicetrue is None:
        return await ctx.send("**Blitz** ne peut pas quitter car il n'est pas dans un salon vocal !")
    await ctx.voice_client.disconnect()
    await ctx.send("**Blitz** a quitté votre *salon vocal* !")


@bot.command()
async def play(ctx, *, url):
    player = music.get_player(guild_id=ctx.guild.id)
    voicetrue = ctx.author.voice
    mevoicetrue = ctx.guild.me.voice
    if voicetrue is None:
        return await ctx.send("**Blitz** ne peut pas se connecter car vous n'êtes pas dans un salon vocal !")
    if mevoicetrue is None:
        await ctx.author.voice.channel.connect()
    else:
        if not player:
            player = music.create_player(ctx, ffmpeg_error_betterfix=True)
        if not ctx.voice_client.is_playing():
            await player.queue(url, search=True)
            song = await player.play()
            await ctx.send(f"**Blitz** joue le son: `{song.name}`")
        else:
            song = await player.queue(url, search=True)
            await ctx.send(f"**Blitz** a ajouté `{song.name}` à la queue !")


@bot.command()
async def p(ctx, *, url):
    player = music.get_player(guild_id=ctx.guild.id)
    voicetrue = ctx.author.voice
    mevoicetrue = ctx.guild.me.voice
    if voicetrue is None:
        return await ctx.send("**Blitz** ne peut pas se connecter car vous n'êtes pas dans un salon vocal !")
    if mevoicetrue is None:
        await ctx.author.voice.channel.connect()
    else:
        pass

    if not player:
        player = music.create_player(ctx, ffmpeg_error_betterfix=True)
    if not ctx.voice_client.is_playing():
        await player.queue(url, search=True)
        song = await player.play()
        await ctx.send(f"**Blitz** joue le son: `{song.name}`")
    else:
        song = await player.queue(url, search=True)
        await ctx.send(f"**Blitz** a ajouté `{song.name}` à la queue !")


@bot.command()
async def queue(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    await ctx.send(f"{' **|** '.join([song.name for song in player.current_queue()])}")


@bot.command()
async def pause(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.pause()
    await ctx.send(f'**Blitz** a mis `{song.name}` mis en pause !')


@bot.command()
async def resume(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.resume()
    await ctx.send(f'**Blitz** a mis `{song.name}` en lecture !')


@bot.command()
async def loop(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.toggle_song_loop()
    if song.is_looping:
        return await ctx.send(f'**Blitz** relance `{song.name}` en *boucle* !')
    else:
        return await ctx.send(f'**Blitz** ne peut pas relancer `{song.name}` !')


@bot.command()
async def nowplaying(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = player.now_playing()
    await ctx.send(f"`{song.name}`")


@bot.command()
async def remove(ctx, index):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.remove_from_queue(int(index))
    await ctx.send(f'**Blitz** a retiré `{song.name}` de la queue')


@bot.command()
async def skip(ctx):
    client = ctx.guild.voice_client
    client.stop()


@bot.command()
async def help(ctx):
    em = discord.Embed(title="Help Blitz",
                       description="Voici la liste des toutes les commandes disponibles avec Blitz:", color=0xFF00D1)
    em.add_field(name="✅ `join`", value="• Rejoint le salon vocal", inline=False)
    em.add_field(name="❌ `leave`", value="• Quitte le salon vocal", inline=False)
    em.add_field(name="🎵 `play <url>`", value="• Joue une musique", inline=False)
    em.add_field(name="⏸️ `pause`", value="• Met en pause la musique", inline=False)
    em.add_field(name="⏯️ `resume`", value="• Relance la musique", inline=False)
    em.add_field(name="⏭️ `skip`", value="• Passe à la musique suivante", inline=False)
    em.add_field(name="🎶 `queue`", value="• Affiche la liste des musiques", inline=False)
    em.add_field(name="🔁 `loop`", value="• Relance la même musique qu'avant", inline=False)
    em.add_field(name="⏺️ `nowplaying`", value="• Affiche la musique en cours", inline=False)
    em.add_field(name="⁉️ `/setprefix <prefix>`", value="• Changer le prefix du bot", inline=False)
    await ctx.send(embed=em)


###########################################################################################

@bot.command()
async def load(ctx, extension):
    try:
        bot.load_extension(extension)
        await ctx.send('Loaded **{}**'.format(extension))
    except Exception as error:
        await ctx.send('**{}** cannot be loaded. [{}]'.format(extension, error))


@bot.command()
async def unload(ctx, extension):
    try:
        bot.unload_extension(extension)
        await ctx.send('Unloaded **{}**'.format(extension))
    except Exception as error:
        await ctx.send('**{}** cannot be unloaded. [{}]'.format(extension, error))


if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print('**{}** cannot be loaded. [{}]'.format(extension, error))


@bot.command()
async def reload(ctx, extension):
    if extension:
        try:
            bot.reload_extension(extension)
            await ctx.send('Reloaded **{}**'.format(extension))
        except:
            bot.load_extension(extension)
            await ctx.send('Loaded **{}**'.format(extension))


bot.run("ODg5NDQ5NzEwMTM2NDcxNTcz.YUhamA.pgvSWDPEIWeHwhqISYztHU1hhcU")
