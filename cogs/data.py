enable=True


import discord
from discord.ext import commands
import random
from discord import app_commands#  增加DC / 指令支援
from function.webhook_DBG import send_DC as DBG
import function.colors as C
import json
import function.data as dta_ctrl
import os


class data_ctrl(commands.Cog):
	bot:commands.Bot
	def __init__(self,bot:commands.Bot):
		#  self: 代表這個class，可以使用class.n的方式呼叫class內的變數
		#  bot: 這個class的變數，代表DCbot
		#  commands.Bot: 代表DCbot的class
		self.bot=bot

	@commands.Cog.listener()
	async def on_ready(self):
		DBG("[cog][data_ctrl]準備完成",bef=C.suc(),aft=C.res())
	
	@app_commands.command(name="save",description="將資料儲存到資料庫")
	async def save(self,interaction:discord.Interaction):
		dta_ctrl.save()
		await interaction.response.send_message("儲存完成")
	
	@app_commands.command(name="recovery",description="回復資料")
	@app_commands.describe(dta="json格式的資料檔案")
	async def recovery(self,interaction:discord.Interaction,dta:str):
		if(interaction.user.id!=int(os.getenv("adminid"))):
			await interaction.response.send_message("你不是bot擁有者，拒絕存取")
			return
		dta_j={}
		try:
			dta_j=json.loads(dta)
			(dta_ctrl.data).update(dta_j)
			dta_ctrl.save()
			await interaction.response.send_message("回復完成")
		except:
			await interaction.response.send_message("回復失敗")
			return
	
	@app_commands.command(name="export",description="匯出資料")
	@app_commands.describe(sp="縮排空格數量",self_channel="是否用私訊")
	async def export(self,interaction:discord.Interaction,sp:int=0,self_channel:bool=True):
		if(interaction.user.id!=int(os.getenv("adminid"))):
			await interaction.response.send_message("你不是bot擁有者，拒絕存取")
			return
		print("匯出中")
		if(sp==0):
			output_dta=json.dumps(dta_ctrl.data,sort_keys=True,allow_nan=True,ensure_ascii=False)
		else:
			output_dta=json.dumps(dta_ctrl.data,indent=sp,sort_keys=True,allow_nan=True,ensure_ascii=False)
		if(self_channel):
			await interaction.user.send(f"```json\n{output_dta}\n```")
			await interaction.response.send_message(f"已私訊")
		else:
			await interaction.response.send_message(f"```json\n{output_dta}\n```")
	
	@app_commands.command(name="reload",description="重新載入")
	async def reload(self,interaction:discord.Interaction):
		if(interaction.user.id!=int(os.getenv("adminid"))):
			await interaction.response.send_message("你不是bot擁有者，拒絕存取")
			return
		dta_ctrl.load()
		await interaction.response.send_message("重新載入完成")

		

async def setup(bot:commands.Bot):
	#  將Cog加入Bot中
	if(not enable):
		return
	await bot.add_cog(data_ctrl(bot))


