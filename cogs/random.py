enable=True


import discord
from discord.ext import commands
import random
from discord import app_commands#  增加DC / 指令支援
from function.webhook_DBG import send_DC as DBG
import function.colors as C

class rand(commands.Cog):
	bot:commands.Bot
	def __init__(self,bot:commands.Bot):
		#  self: 代表這個class，可以使用class.n的方式呼叫class內的變數
		#  bot: 這個class的變數，代表DCbot
		#  commands.Bot: 代表DCbot的class
		self.bot=bot

	@commands.Cog.listener()
	async def on_ready(self):
		DBG("[cog][random]準備完成",bef=C.suc(),aft=C.res())
	
	#  name: 指令名稱
	#  description: 指令描述
	#  p.s. fn名稱沒有規定，但建議使用指令名稱
	@app_commands.command(name="random",description="隨機取數")
	@app_commands.describe(l="左界",r="右界")
	async def random(self,interaction:discord.Interaction,l:int=1,r:int=100):
		if(l>r):
			a=l
			l=r
			r=a
		await interaction.response.send_message(random.randint(l,r))
		

		

async def setup(bot:commands.Bot):
	#  將Cog加入Bot中
	if(not enable):
		return
	await bot.add_cog(rand(bot))