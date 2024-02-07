enable=True


import discord
from discord.ext import commands
import random
from discord import app_commands#  增加DC / 指令支援
from function.webhook_DBG import send_DC as DBG
import function.colors as C

class which(commands.Cog):
	bot:commands.Bot
	def __init__(self,bot:commands.Bot):
		#  self: 代表這個class，可以使用class.n的方式呼叫class內的變數
		#  bot: 這個class的變數，代表DCbot
		#  commands.Bot: 代表DCbot的class
		self.bot=bot

	@commands.Cog.listener()
	async def on_ready(self):
		DBG("[cogs][which]準備完成",bef=C.suc(),aft=C.res())
	
	@commands.Cog.listener()
	async def on_message(self,message:discord.Message):
		if(message.author==self.bot.user):
			return
		# print(message.content[:2])
		# print((message.content[3:]).split())
		if("哪個"in message.content[:2]):
			pass
			lst=(message.content[3:]).split()
			await message.reply(random.choice(lst))

		

async def setup(bot:commands.Bot):
	#  將Cog加入Bot中
	if(not enable):
		return
	DBG("[cogs][which]載入中")
	await bot.add_cog(which(bot))
	DBG("[cogs][which]載入完成")
