import discord
from discord.ext import commands
import json
from discord_slash import cog_ext

class Prefix(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
	    with open("prefixes.json", "r") as f:
	        prefixes = json.load(f)

	    prefixes[str(guild.id)] = "*"

	    with open("prefixes.json", "w") as f:
	        json.dump(prefixes, f, indent = 2)

	@cog_ext.cog_slash(name = "setprefix", description = "Change le prefix du bot.")
	@commands.has_permissions(administrator = True)
	async def setprefix(self, ctx, prefix):
	    with open("prefixes.json", "r") as f:
	        prefixes = json.load(f)

	    prefixes[str(ctx.guild.id)] = prefix

	    with open("prefixes.json", "w") as f:
	        json.dump(prefixes, f, indent = 2)

	    await ctx.send(f"<a:scarycheck:835499517977690122> Le prefix a bien été changé en `{prefix}`")

	@commands.Cog.listener()
	async def on_message(self, msg):

	    try:
	        if msg.mentions[0] == bot.user:

	            with open("prefixes.json", "r") as f:
	                prefixes = json.load(f)

	            pre = prefixes[str(msg.guild.id)]

	            await msg.channel.send(f"Prefix: `{pre}`")

	    except:
	        pass


def setup(bot):
	bot.add_cog(Prefix(bot))