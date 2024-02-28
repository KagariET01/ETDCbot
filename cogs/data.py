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
import requests
from cogs.sudo import sudo_check as su


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
	
	@commands.Cog.listener()
	async def on_message(self,message:discord.Message):
		if(message.author==self.bot.user):
			return
		if(not su(message.author.id)):
			return
		if("recovery" in message.content):
			await message.channel.send("回復中")
			try:
				print("正在獲取檔案，網址：")
				print(message.attachments[0].url)
				
				new_data=requests.get(message.attachments[0].url)
				print("已獲取檔案")
				data_ctrl.data=json.loads(new_data.text)
				print("轉檔成功")
				os.system("rm newdata.json")
				print("快取刪除成功")
				dta_ctrl.save()
				await message.channel.send("回復成功")
			except:
				await message.channel.send("回復失敗")
				return
			
	@app_commands.command(name="recovery",description="回復資料")
	@app_commands.describe(dta="json格式的資料檔案")
	async def recovery(self,interaction:discord.Interaction,dta:str):
		if(not su(interaction.user.id)):
			await interaction.response.send_message("你不是bot擁有者，拒絕存取")
			return
		await interaction.response.send_message("請直接在聊天室輸入`recovery`，並附上檔案以回復資料")
	
	@app_commands.command(name="export",description="匯出資料")
	@app_commands.describe(self_channel="是否用私訊")
	async def export(self,interaction:discord.Interaction,self_channel:bool=True):
		if(not su(interaction.user.id)):
			await interaction.response.send_message("你不是bot擁有者，拒絕存取")
			return
		print("匯出中")
		if(self_channel):
			await interaction.user.send("請查收檔案",file=discord.File(os.getenv("data_path"),filename=os.getenv("data_path").split("/")[-1]))
			await interaction.response.send_message(f"已私訊")
		else:
			await interaction.response.send_message("請查收檔案",file=discord.File(os.getenv("data_path"),filename=os.getenv("data_path").split("/")[-1]))
	
	@app_commands.command(name="reload",description="重新載入")
	async def reload(self,interaction:discord.Interaction):
		if(not su(interaction.user.id)):
			await interaction.response.send_message("你不是bot擁有者，拒絕存取")
			return
		dta_ctrl.load()
		await interaction.response.send_message("重新載入完成")

		

async def setup(bot:commands.Bot):
	#  將Cog加入Bot中
	if(not enable):
		return
	await bot.add_cog(data_ctrl(bot))


