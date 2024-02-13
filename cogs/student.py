enable=True
app_name="student"


import discord
from discord.ext import commands
import random
from discord import app_commands#  增加DC / 指令支援
from function.webhook_DBG import send_DC as DBG
import function.colors as C
import function.data as dta_ctrl

class student(commands.Cog):
	bot:commands.Bot
	def __init__(self,bot:commands.Bot):
		#  self: 代表這個class，可以使用class.n的方式呼叫class內的變數
		#  bot: 這個class的變數，代表DCbot
		#  commands.Bot: 代表DCbot的class
		self.bot=bot

	@commands.Cog.listener()
	async def on_ready(self):
		DBG(f"[cog][{app_name}]準備完成",bef=C.suc(),aft=C.res())
	
	@app_commands.command(name="student_r",description="座號抽籤重製")
	@app_commands.describe(l="第一號",r="最後一號")
	async def reset(self,interaction:discord.Interaction,l:int=1,r:int=30):
		if(l>r):
			l,r=r,l
		gid:str=interaction.guild.id
		cid:str=interaction.channel.id
		if(gid not in dta_ctrl.data):
			dta_ctrl.data[gid]={}
		if(cid not in dta_ctrl.data[gid]):
			dta_ctrl.data[gid][cid]={}
		if("student" not in dta_ctrl.data[gid][cid]):
			dta_ctrl.data[gid][cid]["student"]={}
		dta_ctrl.data[gid][cid]["student"]["get"]=[i for i in range(l,r+1)]
		await interaction.response.send_message(f"座號抽籤重製完成，範圍為{l}~{r}")

	@app_commands.command(name="student_get",description="抽籤")
	async def get(self,interaction:discord.Interaction):
		gid:str=interaction.guild.id
		cid:str=interaction.channel.id
		if(gid not in dta_ctrl.data):
			await interaction.response.send_message("請先使用student_r重製")
			return
		if(cid not in dta_ctrl.data[gid]):
			await interaction.response.send_message("請先使用student_r重製")
			return
		if("student" not in dta_ctrl.data[gid][cid]):
			await interaction.response.send_message("請先使用student_r重製")
			return
		if(len(dta_ctrl.data[gid][cid]["student"]["get"])==0):
			await interaction.response.send_message("座號全部抽完了，請使用student_r重製")
			return
		get=random.choice(dta_ctrl.data[gid][cid]["student"]["get"])
		dta_ctrl.data[gid][cid]["student"]["get"].remove(get)
		await interaction.response.send_message(f"抽到{get}")
		
	@app_commands.command(name="student_see",description="查看誰還沒被抽到過")
	async def see(self,interaction:discord.Interaction):
		gid:str=interaction.guild.id
		cid:str=interaction.channel.id
		if(gid not in dta_ctrl.data):
			await interaction.response.send_message("請先使用student_r重製")
			return
		if(cid not in dta_ctrl.data[gid]):
			await interaction.response.send_message("請先使用student_r重製")
			return
		if("student" not in dta_ctrl.data[gid][cid]):
			await interaction.response.send_message("請先使用student_r重製")
			return
		if(len(dta_ctrl.data[gid][cid]["student"]["get"])==0):
			await interaction.response.send_message("座號全部抽完了")
			return
		restr="剩下這些座號沒被抽到\n"
		c=10
		for i in dta_ctrl.data[gid][cid]["student"]["get"]:
			restr+=f"{i}號 "
			c-=1
			if(c==0):
				restr+="\n"
				c=10
		await interaction.response.send_message(restr)

async def setup(bot:commands.Bot):
	#  將Cog加入Bot中
	if(not enable):
		return	
	DBG(f"[cog][{app_name}]載入中")
	await bot.add_cog(student(bot))
	DBG(f"[cog][{app_name}]載入成功")