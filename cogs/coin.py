enable=True
app_name="coin"


import discord
from discord.ext import commands
import random
from discord import app_commands#  增加DC / 指令支援
from function.webhook_DBG import send_DC as DBG
import function.colors as C
import os
from cogs.sudo import sudo_check as su

coin_list=[
	"擲出金幣：正面","擲出金幣：反面",
	"擲出銀幣：正面","擲出銀幣：反面",
	"擲出銅幣：正面","擲出銅幣：反面",
]

coin_special=[
	"擲出金幣：正面","擲出金幣：反面","擲出金幣：小ㄌㄌ把它撿走了",
	"擲出銀幣：正面","擲出銀幣：反面","擲出銀幣：小ㄌㄌ把它撿走了",
	"擲出銅幣：正面","擲出銅幣：反面","擲出銅幣：小ㄌㄌ把它撿走了",
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
		global coin_list,coin_special
		if(message.author==self.bot.user):
			return
		if(su(message.author.id) and "擲硬幣" in message.content):
			re=random.choice(coin_special)
			DBG(re)
			await message.channel.send(f"{re}")
		if("擲硬幣" in message.content):
			re:str=random.choice(coin_list)
			DBG(re)
			await message.channel.send(f"{re}")

	@app_commands.command(name="coin",description="擲硬幣")
	async def coin(self,interaction:discord.Interaction):
		global coin_list,coin_special
		if(su(interaction.user.id)):
			re=random.choice(coin_special)
			DBG(re)
			await interaction.response.send_message(f"{re}")
		else:
			re=random.choice(coin_list)
			DBG(re)
			await interaction.response.send_message(f"{re}")
	
	

		

async def setup(bot:commands.Bot):
	#  將Cog加入Bot中
	if(not enable):
		return	
	DBG(f"[cog][{app_name}]載入中")
	await bot.add_cog(coin(bot))
	DBG(f"[cog][{app_name}]載入成功")