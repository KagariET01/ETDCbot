enable=False


import discord
from discord.ext import commands
from discord import app_commands#  增加DC / 指令支援
from function.webhook_DBG import send_DC as DBG
import function.colors as C


class eng(commands.Cog):
	bot:commands.Bot
	def __init__(self,bot:commands.Bot):
		#  self: 代表這個class，可以使用class.n的方式呼叫class內的變數
		#  bot: 這個class的變數，代表DCbot
		#  commands.Bot: 代表DCbot的class
		self.bot=bot
	
	@commands.Cog.listener()
	async def on_ready(self):
		# slash = await self.bot.tree.sync()
		DBG("[cog][eng]準備完成",bef=C.suc(),aft=C.res())

	#  name: 指令名稱
	#  description: 指令描述
	#  p.s. fn名稱沒有規定，但建議使用指令名稱
	@app_commands.command(name="eng_c",description="建立新單字表")
	@app_commands.describe(fname="輸入檔名",l1="第一個語言",l2="第二個語言")
	async def hello(self,interaction:discord.Interaction,fname:str,l1:str,l2:str):
		nwf=open(f"data/eng/{interaction.user.id}/{fname}.csv","w+")
		nwf.write(f"{l1},{l2}\n")
		await interaction.response.send_message("單字表建立成功")

		

async def setup(bot:commands.Bot):
	#  將Cog加入Bot中
	if(not enable):
		return
	await bot.add_cog(eng(bot))