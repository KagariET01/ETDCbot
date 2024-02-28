import discord
from discord.ext import commands
from discord import app_commands#  增加DC / 指令支援


cache={}


def key(interaction:discord.Interaction,g=True,c=True):
	re:str=""
	if(g and interaction.guild_id!=None):
		re+=f"guild_{interaction.guild_id}"
		cache[re]=interaction.guild
	elif(c and interaction.channel_id!=None):
		re+=f"channel_{interaction.channel_id}"
		cache[re]=interaction.channel
	else:
		re+=f"user_{interaction.user_id}"
		cache[re]=interaction.user
	return re
		



def rekey(key:str,bot:commands.Bot):
	if(key.startswith("guild_")):
		cache[key]=bot.get_guild(int(key[6:]))
	elif(key.startswith("channel_")):
		cache[key]=bot.get_channel(int(key[8:]))
	else:
		cache[key]=bot.get_user(int(key[5:]))
	return cache[key]