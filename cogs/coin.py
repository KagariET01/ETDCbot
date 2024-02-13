enable=True
app_name="coin"


import discord
from discord.ext import commands
import random
from discord import app_commands#  增加DC / 指令支援
from function.webhook_DBG import send_DC as DBG
import function.colors as C
import os

coin=[
	"擲出金幣：正面","擲出金幣：反面",
	"擲出銀幣：正面","擲出銀幣：反面",
	"擲出銅幣：正面","擲出銅幣：反面",
	"丟出一張小朋友：正面","丟出一張小朋友：反面"
]

coin_special=[
	"擲出金幣：正面","擲出金幣：反面","擲出金幣：小ㄌㄌ把它撿走了",
	"擲出銀幣：正面","擲出銀幣：反面","擲出銀幣：小ㄌㄌ把它撿走了",
	"擲出銅幣：正面","擲出銅幣：反面","擲出銅幣：小ㄌㄌ把它撿走了",
	"丟出一張小朋友：正面","丟出一張小朋友：反面","丟出一張小朋友：小ㄌㄌ把它撿走了"
]



class coin(commands.Cog):
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
		if(message.author.id==os.getenv("adminid")):
			await message.channel.send(f"{random.shuffle(coin_special)[0]}")
		if("擲硬幣" in message.content):
			await message.channel.send(f"{random.shuffle(coin)[0]}")

	
	

		

async def setup(bot:commands.Bot):
	#  將Cog加入Bot中
	if(not enable):
		return	
	DBG(f"[cog][{app_name}]載入中")
	await bot.add_cog(coin(bot))
	DBG(f"[cog][{app_name}]載入成功")