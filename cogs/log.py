enable=True

import discord
from discord.ext import commands
from discord import app_commands#  增加DC / 指令支援
from function.webhook_DBG import send_DC as DBG
from function.webhook_DBG import get_msn,get_user
from colorama import Fore, Style, Back
import function.colors as C
import os


logchannel=os.getenv("logchannel")
try:
	logchannel=int(logchannel)
except:
	logchannel=0

class DClog(commands.Cog):
	bot:commands.Bot
	def __init__(self,bot:commands.Bot):
		#  self: 代表這個class，可以使用class.n的方式呼叫class內的變數
		#  bot: 這個class的變數，代表DCbot
		#  commands.Bot: 代表DCbot的class
		self.bot=bot
	
	@commands.Cog.listener()
	async def on_ready(self):
		get_user(self.bot.user)
		DBG("[cog][log]準備完成",bef=C.suc(),aft=C.res())
		

	@commands.Cog.listener()
	async def on_message(self,message:discord.Message):
		#print("[cogs][log][on_message]觸發")
		try:
			if(message.channel.id==logchannel):
				#print("[cogs][log][on_message]測試頻道，不處理")
				return
			get_msn(message)
		except:
			#print("[cogs][log][on_message]發生錯誤")
			DBG("[cogs][log][on_message][ERROR]發生錯誤",bef=C.err(),aft=C.res())

async def setup(bot:commands.Bot):
	#  將Cog加入Bot中
	if(not enable):
		return
	DBG("[cogs][log]載入中")
	await bot.add_cog(DClog(bot))
	DBG("[cogs][log]載入成功")