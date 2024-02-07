enable=True


import discord
from discord.ext import commands
from discord import app_commands#  增加DC / 指令支援
from function.webhook_DBG import send_DC as DBG
import function.colors as C
import random

dta=[
	{
		"key":"是不是",
		"re":[
			"是",
			"不是",
			"問就是是",
			"問就是不是",
		]
	},
	{
		"key":"要不要",
		"re":[
			"要",
			"不要",
			"問就是要",
			"問就是不要",
			"傑哥不要",
			"傑哥我要（製作組：？",
		]
	},
	{
		"key":"有沒有",
		"re":[
			"有",
			"沒有",
			"問就是有",
			"問就是沒有"
		]
	},
]


class tf(commands.Cog):
	bot:commands.Bot
	def __init__(self,bot:commands.Bot):
		#  self: 代表這個class，可以使用class.n的方式呼叫class內的變數
		#  bot: 這個class的變數，代表DCbot
		#  commands.Bot: 代表DCbot的class
		self.bot=bot
	
	@commands.Cog.listener()
	async def on_ready(self):
		# slash = await self.bot.tree.sync()
		DBG("[Cog][tf]準備完成",bef=C.suc(),aft=C.res())

	@commands.Cog.listener()
	async def on_message(self,message:discord.Message):
		if(message.author==self.bot.user):
			return
		for i in dta:
			if(i["key"]in(message.content)):
				await message.reply(random.choice(i["re"]))
				return
		

async def setup(bot:commands.Bot):
	#  將Cog加入Bot中
	if(not enable):
		return
	await bot.add_cog(tf(bot))