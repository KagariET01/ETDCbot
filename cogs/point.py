enable=True
app_name="point"


import discord
from discord.ext import commands
import random
from discord import app_commands#  增加DC / 指令支援
from function.webhook_DBG import send_DC as DBG
import function.colors as C
import function.data as dta_ctrl

class point(commands.Cog):
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
		gid:str=str(message.guild.id)
		if(not gid in dta_ctrl.data):
			dta_ctrl.data[gid]={}
		if(not "point" in dta_ctrl.data[gid]):
			dta_ctrl.data[gid]["point"]={}
		dta_ctrl.data[gid]["point"]
		uid:str=str(message.author.id)
		if(not uid in dta_ctrl.data[gid]["point"]):
			dta_ctrl.data[gid]["point"][uid]=0
		dta_ctrl.data[gid]["point"][uid]+=len(message.content)
	

		

async def setup(bot:commands.Bot):
	#  將Cog加入Bot中
	if(not enable):
		return	
	DBG(f"[cog][{app_name}]載入中")
	await bot.add_cog(point(bot))
	DBG(f"[cog][{app_name}]載入成功")