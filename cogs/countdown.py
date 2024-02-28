enable=True
app_name="countdown"


import discord
from discord.ext import commands
import random
from discord import app_commands#  增加DC / 指令支援
from function.webhook_DBG import send_DC as DBG
import function.colors as C
import function.data as dta_ctrl
from function.get_key import key,rekey
import datetime
import asyncio
from discord.ext import tasks
import os

class cd(commands.Cog):
	bot:commands.Bot
	def __init__(self,bot:commands.Bot):
		#  self: 代表這個class，可以使用class.n的方式呼叫class內的變數
		#  bot: 這個class的變數，代表DCbot
		#  commands.Bot: 代表DCbot的class
		self.bot=bot

	countlist=[]
	
	@app_commands.command(name="countdown_add",description="新增倒數機器")
	@app_commands.describe(year="事件時間（年）",month="事件時間（月）",day="事件時間（日）",hour="發送時間（時）",minute="發送時間（分）",name="事件名稱")
	async def add_event(self,interaction:discord.Interaction,
		year:int,
		month:int,
		day:int,
		hour:int,
		minute:int,
		name:str="倒數計時器"
	):
		gid:str=key(interaction)
		DBG(f"{gid} 新增倒數機器")
		if(not gid in dta_ctrl.data):
			dta_ctrl.data[gid]={}
		if(not "countdown" in dta_ctrl.data[gid]):
			dta_ctrl.data[gid]["countdown"]=[]
		dta_ctrl.data[gid]["countdown"].append({
			"Y":year,
			"M":month,
			"D":day,
			"h":hour,
			"m":minute,
			"name":name
		})
		dta_ctrl.save()
		
		await interaction.response.send_message("倒數機器新增完成")

	@app_commands.command(name="countdown_del",description="刪除倒數機器")
	@app_commands.describe(name="事件名稱")
	async def delete_event(self,interaction:discord.Interaction,name:str):
		gid:str=key(interaction,False)
		DBG(f"{gid} 刪除倒數機器")
		if(not gid in dta_ctrl.data):
			return
		if(not "countdown" in dta_ctrl.data[gid]):
			return
		for i in dta_ctrl.data[gid]["countdown"]:
			if(i["name"]==name):
				dta_ctrl.data[gid]["countdown"].remove(i)
				break
		dta_ctrl.save()
		ch=None
		if(interaction.channel!=None):
			ch=interaction.channel
		else:
			ch=interaction.user

		for i in self.countlist:
			if(i["name"]==name and i["channel"]==ch):
				self.countlist.remove(i)
				break
		await interaction.response.send_message("倒數機器刪除完成")


	@tasks.loop(minutes=1)
	async def countdown(self):
		self.countlist=[]
		for i in dta_ctrl.data:
			if(not "countdown" in dta_ctrl.data[i]):
				continue
			ch=rekey(i,self.bot)
			if(ch==None):
				continue
			for j in dta_ctrl.data[i]["countdown"]:
				now=datetime.datetime.now()+datetime.timedelta(hours=int(os.getenv("timezone")))
				event_time=datetime.datetime(j["Y"],j["M"],j["D"],j["h"],j["m"],59)
				if(event_time<now):
					dta_ctrl.data[i]["countdown"].remove(j)
					continue
				self.countlist.append({
					"event_time":event_time,
					"next_send_time":event_time,
					"channel":ch,
					"name":j["name"]
				})

		now_y=datetime.datetime.now().year
		now_m=datetime.datetime.now().month
		now_d=datetime.datetime.now().day
		today=datetime.datetime(now_y,now_m,now_d,0,0,0)
		now=datetime.datetime.now()+datetime.timedelta(hours=int(os.getenv("timezone")))
		for i in self.countlist:
			if(i["event_time"]<today):
				self.countlist.remove(i)
				continue
			if(i["next_send_time"]<=now):
				d=(i['event_time']-today).days
				emb=discord.Embed(title=f"{i['name']}",description=f"還有 {d} 天",color=0x00ffff)
				await i["channel"].send(embed=emb)
				i["next_send_time"]=i["next_send_time"]+datetime.timedelta(days=1)
		print(f"countdown:{len(self.countlist)}")

	@commands.Cog.listener()
	async def on_ready(self):
		self.countdown.start()
		DBG(f"[cog][{app_name}]準備完成",bef=C.suc(),aft=C.res())

		

async def setup(bot:commands.Bot):
	#  將Cog加入Bot中
	if(not enable):
		return	
	DBG(f"[cog][{app_name}]載入中")
	await bot.add_cog(cd(bot))
	DBG(f"[cog][{app_name}]載入成功")