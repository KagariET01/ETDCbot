enable=True
app_name="sudo"

"""
sudo 超級權限
資料庫:不使用，程式關閉後立即失效
指令:
/sudo 獲取sudo超級權限
/sudo_exit 解除sudo超級權限
/sudo_get_otp 獲取sudo單次金鑰（金鑰有效時間以金鑰生成時間計算）
"""


import discord
from discord.ext import commands
import random
from discord import app_commands#  增加DC / 指令支援
from function.webhook_DBG import send_DC as DBG
import function.colors as C
import function.data as dta_ctrl
import hashlib
import string
from datetime import datetime,timedelta
import os

admin={}

def sudo_check(id):
	if(id in admin):
		nowtime:datetime=datetime.now()
		if(nowtime<admin[id]):
			return True
		else:
			admin.pop(id)
			return False
	return False

class sudo(commands.Cog):
	bot:commands.Bot
	def __init__(self,bot:commands.Bot):
		#  self: 代表這個class，可以使用class.n的方式呼叫class內的變數
		#  bot: 這個class的變數，代表DCbot
		#  commands.Bot: 代表DCbot的class
		self.bot=bot
		global admin
		adminlst=os.getenv("adminid").split(",")
		DBG(adminlst)
		for i in adminlst:
			admin[int(i)]=datetime.now()+timedelta(days=3650)
		DBG(admin)

	key={}

	@commands.Cog.listener()
	async def on_ready(self):
		DBG(f"[cog][{app_name}]準備完成",bef=C.suc(),aft=C.res())
	
	@commands.Cog.listener()
	async def on_message(self,message:discord.Message):
		if(message.author==self.bot.user):
			return
	
	

	@app_commands.command(name="sudo",description="獲取sudo超級權限")
	@app_commands.describe(key="驗證金鑰")
	async def gsudo(self,interaction:discord.Interaction,key:str=""):
		global admin
		key=hashlib.sha256(key.encode()).hexdigest()
		if(key in self.key):
			admin[interaction.user.id]=self.key[key]
			self.key.pop(key)
			await interaction.response.send_message(f"成功獲得sudo權限\n記住：權限越大，責任越大\n時限只到<t:{int(admin[interaction.user.id].timestamp())}:f>")
		else:
			await interaction.response.send_message(f"金鑰錯誤")
		pass
	
	@app_commands.command(name="sudo_exit",description="解除sudo超級權限")
	async def sudo(self,interaction:discord.Interaction):
		global admin
		if(interaction.user.id == os.getenv("adminid")):
			await interaction.response.send_message(f"機器人擁有者不能解除sudo權限")
			return
		if(sudo_check(interaction.user.id)):
			admin.pop(interaction.user.id)
			await interaction.response.send_message(f"成功解除sudo權限")
		pass

	@app_commands.command(name="sudo_get_otp",description="獲取sudo單次金鑰")
	@app_commands.describe(time_m="有效時間(分鐘)")
	async def get_otp(self,interaction:discord.Interaction,time_m:int=10):
		global admin
		if(sudo_check(interaction.user.id)):
			key=""
			for _ in range(16):
				key+=random.choice(string.ascii_letters+string.digits+string.ascii_lowercase+string.ascii_uppercase)
			self.key[hashlib.sha256(key.encode()).hexdigest()]=datetime.now()+timedelta(minutes=time_m)
			await interaction.response.send_message(f"請至私訊取得金鑰")
			await interaction.user.send(f"你的金鑰是：")
			await interaction.user.send(f"{key}")
			await interaction.user.send(f"請保管好你的金鑰")
		else:
			await interaction.response.send_message(f"你沒有sudo權限")

		

async def setup(bot:commands.Bot):
	#  將Cog加入Bot中
	if(not enable):
		return	
	DBG(f"[cog][{app_name}]載入中")
	await bot.add_cog(sudo(bot))
	DBG(f"[cog][{app_name}]載入成功")