enable=True


import discord
from discord.ext import commands
from discord import app_commands#  增加DC / 指令支援
from function.webhook_DBG import send_DC as DBG
import function.colors as C
import random
import os
import time
import function.data as dta_ctrl
import copy
from function.get_key import key
from cogs.sudo import sudo_check as su



class main(commands.Cog):
	bot:commands.Bot
	def __init__(self,bot:commands.Bot):
		#  self: 代表這個class，可以使用class.n的方式呼叫class內的變數
		#  bot: 這個class的變數，代表DCbot
		#  commands.Bot: 代表DCbot的class
		self.bot=bot
		self.l=3

	# price={}#  每張抽獎券的獎項
	# lf={}#  剩下的獎的數量
	# c={}#  是否已經抽過

	@commands.Cog.listener()
	async def on_ready(self):
		DBG("[cog][2fan]準備完成",bef=C.suc(),aft=C.res())

	#  name: 指令名稱
	#  description: 指令描述
	#  p.s. fn名稱沒有規定，但建議使用指令名稱
	@app_commands.command(name="2fan_r",description="二番賞重製")
	@app_commands.describe(lst="清單，逗點分隔，代表每個獎勵的數量，左邊代表最好的獎")
	async def fan_r(self,interaction:discord.Interaction,lst:str):
		gid:str=key(interaction)
		DBG(f"{gid} 二番賞重製")
		lst=lst.split(',')
		lst=[int(i) for i in lst]
		if(not gid in dta_ctrl.data):
			dta_ctrl.data[gid]={}
		dta_ctrl.data[gid]["2fan"]={}
		dta_ctrl.data[gid]["2fan"]["price_left"]=lst
		dta_ctrl.data[gid]["2fan"]["price"]=[]
		for i in range(len(lst)):
			for j in range(lst[i]):
				dta_ctrl.data[gid]["2fan"]["price"].append(i)
		random.shuffle(dta_ctrl.data[gid]["2fan"]["price"])
		dta_ctrl.data[gid]["2fan"]["check"]=[False]*len(dta_ctrl.data[gid]["2fan"]["price"])
		dta_ctrl.save()
		await interaction.response.send_message("二番賞重製完成")

	@app_commands.command(name="2fan_see",description="查看還可以抽的獎項")
	async def fan_see(self,interaction:discord.Interaction):
		gid:str=key(interaction)
		if(not gid in dta_ctrl.data or not "2fan" in dta_ctrl.data[gid]):
			await interaction.response.send_message("請先使用 /2fan_r 重製")
			return
		
		l:str=dta_ctrl.data[gid]["2fan"]["price_left"][-1]
		l=len(str(l))
		restr="各個獎項剩餘數量如下\n"
		for i in range(1,len(dta_ctrl.data[gid]["2fan"]["price_left"])+1,1):
			nw=dta_ctrl.data[gid]["2fan"]['price_left'][i-1]
			restr+=f"{i}. {nw}個\n"

		restr+="可抽的編號：\n```txt\n"
		cnt=0
		for i in range(0,len(dta_ctrl.data[gid]["2fan"]['price']),1):
			if(i>=len(dta_ctrl.data[gid]["2fan"]['price'])):
				break
			if(dta_ctrl.data[gid]["2fan"]['check'][i]):
				continue
			restr+=f"[{i+1:>{l}}] "
			cnt+=1
			if(cnt==10):
				restr+="\n"
				cnt=0
		restr+="\n```"
		print(f"{gid}傳送二番賞see資料中")
		await interaction.response.send_message(restr)


	@app_commands.command(name="2fan_get",description="抽獎")
	@app_commands.describe(id="要抽的編號")
	async def fan_get(self,interaction:discord.Interaction,id:int):
		gid:str=key(interaction)
		if(not gid in dta_ctrl.data or not "2fan" in dta_ctrl.data[gid]):
			await interaction.response.send_message("請先使用 /2fan_r 重製")
			return
		if(id<1 or id>len(dta_ctrl.data[gid]["2fan"]['price'])):
			await interaction.response.send_message("編號太小或太大")
			return
		if(dta_ctrl.data[gid]["2fan"]['check'][id-1]):
			await interaction.response.send_message("這個獎項已經被抽過了")
			return
		dta_ctrl.data[gid]["2fan"]['check'][id-1]=True
		l=self.l
		getnum=dta_ctrl.data[gid]["2fan"]['price'][id-1]+1
		dta_ctrl.data[gid]["2fan"]['check'][id-1]=True
		dta_ctrl.data[gid]["2fan"]['price_left'][dta_ctrl.data[gid]["2fan"]['price'][id-1]]-=1
		dta_ctrl.save()
		await interaction.response.send_message(f"恭喜{interaction.user.mention}抽到了 {getnum}獎\n`[ {id:>{l}} => {getnum} ]`")

	@app_commands.command(name="2fan_hack",description="查看每個編號對應的獎項")
	async def fan_hack(self,interaction:discord.Interaction):
		gid:str=key(interaction)
		if(not gid in dta_ctrl.data or not "2fan" in dta_ctrl.data[gid]):
			await interaction.response.send_message("請先使用 /2fan_r 重製")
			return
		l=self.l
		restr=f"{interaction.guild.name} 的二番賞hack如下\n"
		cnt=0
		for i in range(len(dta_ctrl.data[gid]["2fan"]['price'])):
			if(i>=len(dta_ctrl.data[gid]["2fan"]['price'])):
				break
			pricenum=dta_ctrl.data[gid]["2fan"]['price'][i]
			if(dta_ctrl.data[gid]["2fan"]['check'][i]):
				
				restr+=f"[ --- {pricenum} ] "
			else:
				restr+=f"[ {(i+1):>{l}} => {pricenum} ] "
			cnt+=1
			if(cnt==10):
				restr+="\n"
				cnt=0
		if(interaction.permissions.administrator or su(interaction.user.id)):
			await interaction.user.send(f"```\n{restr}\n```")
			se=await interaction.response.send_message("已私訊給你，請查收")
		else:
			await interaction.response.send_message("你沒有權限")

	

async def setup(bot:commands.Bot):
	#  將Cog加入Bot中
	if(not enable):
		return
	DBG("[cogs][2fan]載入中")
	await bot.add_cog(main(bot))
	DBG("[cogs][2fan]載入成功")
