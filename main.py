import discord
from discord.ext import commands
import os
import json
import asyncio
from function.webhook_DBG import send_DC as DBG
from function.webhook_DBG import get_msn,get_user
import function.colors as C
import time
import function.data as dta_ctrl
import asyncio
import threading

token=os.getenv("DCtoken")
logchannel=os.getenv("logchannel")
try:
	logchannel=int(logchannel)
except:
	logchannel=0

#  設定bot權限
intents=discord.Intents.all()
DCbot=commands.Bot(command_prefix="/",intents=intents)


@DCbot.event
async def on_ready():#  DCbot啟動
	DBG("[main]正在載入data.json")
	
	dta_ctrl.load()
	
	DBG("[main]載入/指令中")
	slash=await DCbot.tree.sync()#  增加DC / 指令支援
	DBG("[main]/指令載入完畢")
	
	DBG("===[機器人可以開始使用]===",bef=C.suc(),aft=C.res())
	
	# DBG("[main]bot已啟動，身分為："+str(DCbot.user))
	
	DBG(f"[main]載入 {len(slash)} 個斜線指令")
	str=""
	for i in slash:
		str+=f"/{i.name}\n"
		DBG(i.name)
	await DCbot.change_presence(status=discord.Status.online,activity=discord.Game("更新：即停系統"))
	threading.Thread(target=dta_ctrl.save,args=()).start()
	# await DCbot.get_channel(logchannel).send("雞雞人已啟動，身分為："+str(DCbot.user))
	

	#await DCbot.get_channel(logchannel).send(message.author.name+"說：```\n"+message.content+"```")



protect=False


async def load_file():#  load all cogs
	for fname in os.listdir("./cogs"):
		if(protect):
			try:
				if fname.endswith(".py"):
					# print("loading",fname)
					await DCbot.load_extension(f"cogs.{fname[:-3]}")#  load cog
				pass
			except:
				DBG(f"[main]cogs{fname}載入失敗",bef=C.err(),aft=C.res())
		else:
			if fname.endswith(".py"):
					# print("loading",fname)
					await DCbot.load_extension(f"cogs.{fname[:-3]}")#  load cog
async def main(DCbot):
	DBG("[main]正在載入cogs")
	await load_file()
	DBG("[main]cogs載入完畢")
	

DBG("[main]程式開始執行")
asyncio.run(main(DCbot))
DBG("[main]正在啟動bot")
DCbot.run(token)




