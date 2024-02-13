enable=False
app_name="tools"


import discord
from discord.ext import commands
import random
from discord import app_commands#  增加DC / 指令支援
from function.webhook_DBG import send_DC as DBG
import function.colors as C
import function.data as dta_ctrl
import os
import datetime
import time

class tools(commands.Cog):
	bot:commands.Bot
	def __init__(self,bot:commands.Bot):
		#  self: 代表這個class，可以使用class.n的方式呼叫class內的變數
		#  bot: 這個class的變數，代表DCbot
		#  commands.Bot: 代表DCbot的class
		self.bot=bot
	code={}
	time={}
	@commands.Cog.listener()
	async def on_ready(self):
		DBG(f"[cog][{app_name}]準備完成",bef=C.suc(),aft=C.res())
	
	@app_commands.command(name="tool_clear",description="清空聊天欄")
	@app_commands.describe(channel_name="頻道名",check_code="確認碼",focus="機器人管理員強制執行")
	async def clear(self,interaction:discord.Interaction,channel_name:str,check_code:int=0,focus:bool=False):
		if(not(interaction.user.id==int(os.getenv("adminid")) and focus) and not interaction.permissions.administrator and not interaction.permissions.manage_messages):
			await interaction.response.send_message("你沒有權限，拒絕存取")
			return
		if(channel_name!=interaction.channel.name):
			await interaction.response.send_message("頻道名稱錯誤")
			return
		if(check_code==0):
			self.code[interaction.channel_id]=random.randint(100000,999999)
			self.time[interaction.channel_id]=datetime.datetime.now()
			await interaction.response.send_message(f"請在一分鐘內再次輸入以確認，驗證碼{self.code[interaction.channel_id]}")
		elif(self.code[interaction.channel_id]==check_code and datetime.datetime.now()-self.time[interaction.channel_id]<datetime.timedelta(minutes=1)):
			await interaction.response.send_message("正在清空中")
			channel=await self.bot.fetch_channel(interaction.channel_id)
			async for message in channel.history(limit=10000):
				try:
					await message.delete()
				except:
					break
				time.sleep(0.75)
			await interaction.channel.send_message("清空完成")
		else:
			await interaction.response.send_message("驗證碼錯誤")
	

	@app_commands.command(name="tool_cancel",description="清空聊天欄")
	@app_commands.describe(focus="機器人管理員強制執行")
	async def cancel(self,interaction:discord.Interaction,focus:bool=False):
		if(not(interaction.user.id==int(os.getenv("adminid")) and focus) and not interaction.permissions.administrator and not interaction.permissions.manage_messages):
			await interaction.response.send_message("你沒有權限，拒絕存取")
			return
		self.code[interaction.channel_id]=0
		self.time[interaction.channel_id]=datetime.datetime.now()-datetime.timedelta(days=1)
		await interaction.response.send_message("已取消所有動作")
	

		

async def setup(bot:commands.Bot):
	#  將Cog加入Bot中
	if(not enable):
		return	
	DBG(f"[cog][{app_name}]載入中")
	await bot.add_cog(tools(bot))
	DBG(f"[cog][{app_name}]載入成功")