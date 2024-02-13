enable=False
app_name="ex"


import discord
from discord.ext import commands
import random
from discord import app_commands#  增加DC / 指令支援
from function.webhook_DBG import send_DC as DBG
import function.colors as C
import function.data as dta_ctrl


class which(commands.Cog):
	bot:commands.Bot
	def __init__(self,bot:commands.Bot):
		#  self: 代表這個class，可以使用class.n的方式呼叫class內的變數
		#  bot: 這個class的變數，代表DCbot
		#  commands.Bot: 代表DCbot的class
		self.bot=bot

	@commands.Cog.listener()
	async def on_ready(self):
		DBG(f"[cog][{app_name}]準備完成",bef=C.suc(),aft=C.res())
	
	@commands.Cog.listener()
	async def on_message(self,message:discord.Message):
		if(message.author==self.bot.user):
			return
	
	@app_commands.command(name="2fan_r",description="二番賞重製")
	@app_commands.describe(l="左界",r="右界")
	async def random(self,interaction:discord.Interaction,l:int=1,r:int=100):
		pass
	

		

async def setup(bot:commands.Bot):
	#  將Cog加入Bot中
	if(not enable):
		return	
	DBG(f"[cog][{app_name}]載入中")
	await bot.add_cog(which(bot))
	DBG(f"[cog][{app_name}]載入成功")