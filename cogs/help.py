enable=True


import discord
from discord.ext import commands
import random
from discord import app_commands#  增加DC / 指令支援
from function.webhook_DBG import send_DC as DBG
import function.colors as C

class help(commands.Cog):
	bot:commands.Bot
	def __init__(self,bot:commands.Bot):
		#  self: 代表這個class，可以使用class.n的方式呼叫class內的變數
		#  bot: 這個class的變數，代表DCbot
		#  commands.Bot: 代表DCbot的class
		self.bot=bot

	@commands.Cog.listener()
	async def on_ready(self):
		DBG("[cog][help]準備完成",bef=C.suc(),aft=C.res())

	@app_commands.command(name="help",description="救命")
	async def help(self,interaction:discord.Interaction):
		await interaction.response.send_message(f"{self.bot.user.mention}來救你了！")




async def setup(bot:commands.Bot):
	#  將Cog加入Bot中
	if(not enable):
		return
	await bot.add_cog(help(bot))