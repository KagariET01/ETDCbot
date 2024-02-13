enable=True
app_name="dice"


import discord
from discord.ext import commands
import random
from discord import app_commands#  增加DC / 指令支援
from function.webhook_DBG import send_DC as DBG
import function.colors as C
import function.data as dta_ctrl


class dice(commands.Cog):
	bot:commands.Bot
	def __init__(self,bot:commands.Bot):
		#  self: 代表這個class，可以使用class.n的方式呼叫class內的變數
		#  bot: 這個class的變數，代表DCbot
		#  commands.Bot: 代表DCbot的class
		self.bot=bot

	@commands.Cog.listener()
	async def on_ready(self):
		DBG(f"[cog][{app_name}]準備完成",bef=C.suc(),aft=C.res())
	
	@app_commands.command(name="dice",description="擲骰子")
	@app_commands.describe(count="骰子數")
	async def dice(self,interaction:discord.Interaction,count:int=1):
		if(count<1):
			count=1
		re:str="擲出："
		c=10
		ans=0
		for i in range(count):
			a=random.randint(1,6)
			ans+=a
			re+=f"{a} "
			c-=1
			if(c==0):
				re+="\n"
				c=10
		re+=f"\n總計{ans}點"
		await interaction.response.send_message(re)

		

async def setup(bot:commands.Bot):
	#  將Cog加入Bot中
	if(not enable):
		return	
	DBG(f"[cog][{app_name}]載入中")
	await bot.add_cog(dice(bot))
	DBG(f"[cog][{app_name}]載入成功")