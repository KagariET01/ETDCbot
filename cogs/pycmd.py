enable=True


import discord
from discord.ext import commands
import random
from discord import app_commands#  增加DC / 指令支援
from function.webhook_DBG import send_DC as DBG
import function.colors as C
import os

class pycmd(commands.Cog):
	bot:commands.Bot
	def __init__(self,bot:commands.Bot):
		#  self: 代表這個class，可以使用class.n的方式呼叫class內的變數
		#  bot: 這個class的變數，代表DCbot
		#  commands.Bot: 代表DCbot的class
		self.bot=bot

	@commands.Cog.listener()
	async def on_ready(self):
		DBG("[cog][cmds]準備完成",bef=C.suc(),aft=C.res())
	
	@commands.Cog.listener()
	async def on_message(self,message:discord.Message):
		return
	
	@app_commands.command(name="cmd",description="Py Command")
	@app_commands.describe(c="command")
	async def cmd(self,interaction:discord.Interaction,c:str):
		if(interaction.user.id!=int(os.getenv("adminid"))):
			await interaction.response.send_message("你不是bot擁有者，拒絕存取")
			return
		try:
			await interaction.response.send_message(f"input\n```py\n{c}\n```\noutput\n```txt\n{eval(c)}\n```")
		except:
			await interaction.response.send_message(f"input\n```py\n{c}\n```\noutput\nRunTimeError")
		pass
	

		

async def setup(bot:commands.Bot):
	#  將Cog加入Bot中
	if(not enable):
		return
	await bot.add_cog(pycmd(bot))