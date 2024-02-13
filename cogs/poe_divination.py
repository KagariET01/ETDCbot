enable=True
app_name="poe"


import discord
from discord.ext import commands
import random
from discord import app_commands#  增加DC / 指令支援
from function.webhook_DBG import send_DC as DBG
import function.colors as C


res=[
	"聖杯",
	"笑杯",
	"陰杯"
]


class poe(commands.Cog):
	bot:commands.Bot
	def __init__(self,bot:commands.Bot):
		#  self: 代表這個class，可以使用class.n的方式呼叫class內的變數
		#  bot: 這個class的變數，代表DCbot
		#  commands.Bot: 代表DCbot的class
		self.bot=bot
		self.dta={}

	@commands.Cog.listener()
	async def on_ready(self):
		DBG(f"[cog][{app_name}]準備完成",bef=C.suc(),aft=C.res())
	
	@commands.Cog.listener()
	async def on_message(self,message:discord.Message):
		if(message.author==self.bot.user):
			return
	
	@app_commands.command(name="poe",description="擲筊")
	async def poe(self,interaction:discord.Interaction):
		g=random.randint(0,2)
		if(g==0):
			if(interaction.user.id not in self.dta):
				self.dta[interaction.user.id]=0
			self.dta[interaction.user.id]+=1
			await interaction.response.send_message(f"連續{self.dta[interaction.user.id]}次擲出{res[g]}")
		else:
			await interaction.response.send_message(f"擲出{res[g]}")
			if((interaction.user.id) in self.dta):
				self.dta[interaction.user.id]=0
			

		

async def setup(bot:commands.Bot):
	#  將Cog加入Bot中
	if(not enable):
		return	
	DBG(f"[cog][{app_name}]載入中")
	await bot.add_cog(poe(bot))
	DBG(f"[cog][{app_name}]載入成功")