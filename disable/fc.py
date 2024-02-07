#  file controler

enable=False


import discord
from discord.ext import commands
from discord import app_commands#  增加DC / 指令支援

class fc(commands.Cog):
	bot:commands.Bot
	def __init__(self,bot:commands.Bot):
		#  self: 代表這個class，可以使用class.n的方式呼叫class內的變數
		#  bot: 這個class的變數，代表DCbot
		#  commands.Bot: 代表DCbot的class
		self.bot=bot
	
	#  name: 指令名稱
	#  description: 指令描述
	#  p.s. fn名稱沒有規定，但建議使用指令名稱
	@app_commands.command(name="random",description="Hello, world!")
	@app_commands.describe(l="左界",r="右界")
	async def hello(self,interaction:discord.Interaction):
		print("user send message")

		

async def setup(bot:commands.Bot):
	#  將Cog加入Bot中
	if(not enable):
		return
	await bot.add_cog(fc(bot))