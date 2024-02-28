enable=True

import discord
from discord.ext import commands
from discord import app_commands#  增加DC / 指令支援
from function.webhook_DBG import send_DC as DBG
from function.webhook_DBG import get_msn,get_user
import function.colors as C
import os
from cogs.sudo import sudo_check as su

class pet(commands.Cog):
	bot:commands.Bot
	adminid:int
	def __init__(self,bot:commands.Bot):
		self.bot=bot
		self.adminid=int(os.getenv("adminid"))
	
	@commands.Cog.listener()
	async def on_ready(self):
		DBG("[cog][pet][success]準備完成",bef=C.suc(),aft=C.res())

	@commands.Cog.listener()
	async def on_message(self,message:discord.Message):
		if(self.bot.user in message.mentions):
			if("我喜歡你"in(message.content)):
				if(su(message.author.id)):
					await message.reply("我也喜歡你歐，"+message.author.mention)
				else:
					pass
			if("安"in(message.content)):
				await message.reply("早安，"+message.author.mention)
			

async def setup(bot:commands.Bot):
	#  將Cog加入Bot中
	if(not enable):
		return
	DBG("[cogs][pet]載入中")
	await bot.add_cog(pet(bot))
	DBG("[cogs][pet]載入成功")