import discord
from discord.ext import commands
from discord import app_commands#  增加DC / 指令支援

def key(interaction:discord.Interaction,g=True,c=True):
	re:str=""
	if(g and interaction.guild_id!=None):
		re+=f"guild_{interaction.guild_id}"
		return re
	elif(c and interaction.channel_id!=None):
		re+=f"channel_{interaction.channel_id}"
		return re
	else:
		re+=f"user_{interaction.user_id}"
		return re
		