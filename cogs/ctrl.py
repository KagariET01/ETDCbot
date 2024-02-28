enable=True
name="ctrl"


import discord
from discord.ext import commands
import random
from discord import app_commands#  增加DC / 指令支援
from function.webhook_DBG import send_DC as DBG
import function.colors as C
import os
import datetime
from cogs.sudo import sudo_check as su

class ctrl(commands.Cog):
	bot:commands.Bot
	def __init__(self,bot:commands.Bot):
		#  self: 代表這個class，可以使用class.n的方式呼叫class內的變數
		#  bot: 這個class的變數，代表DCbot
		#  commands.Bot: 代表DCbot的class
		self.bot=bot
	
	time:datetime.datetime=None
	code:int=1

	@commands.Cog.listener()
	async def on_ready(self):
		DBG(f"[cog][{name}]準備完成",bef=C.suc(),aft=C.res())
	
	@commands.Cog.listener()
	async def on_message(self,message:discord.Message):
		if(message.author==self.bot.user):
			return
	
	@app_commands.command(name="ctrl_stop",description="緊急停止")
	@app_commands.describe(code="輸入確認碼")
	async def ctrl_stop(self,interaction:discord.Interaction,code:int=0):
		if(not su(interaction.user.id)):
			await interaction.response.send_message("你不是bot擁有者，拒絕存取")
			return
		if(self.time==None or datetime.datetime.now()-self.time>datetime.timedelta(minutes=1)):
			self.time=datetime.datetime.now()
			self.code=random.randint(100000,999999)
			await interaction.response.send_message(f"請在一分鐘內再次輸入以確認，驗證碼{self.code}")
		elif(code==self.code):
			await interaction.response.send_message("正在停止中")
			await self.bot.close()
			
	

		

async def setup(bot:commands.Bot):
	#  將Cog加入Bot中
	if(not enable):
		return	
	DBG(f"[cogs][{name}]載入中")
	await bot.add_cog(ctrl(bot))
	DBG(f"[cogs][{name}]載入成功")