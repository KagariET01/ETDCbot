enable=False


import discord
from discord.ext import commands
from discord import app_commands#  增加DC / 指令支援

class auto_vchannel(commands.Cog):
	bot:commands.Bot
	def __init__(self,bot:commands.Bot):
		#  self: 代表這個class，可以使用class.n的方式呼叫class內的變數
		#  bot: 這個class的變數，代表DCbot
		#  commands.Bot: 代表DCbot的class
		self.bot=bot
	
	@commands.Cog.listener()
	async def on_ready(self):
		print("[cog][outo_vchannel] on_ready")

	@commands.Cog.listener()
	async def on_voice_state_update(self,member,before,after):
		print("on_voice_state_update")
		if(after.channel.id==1191967367853514843):
			print("==DOIT==")
			new_channel=await bot.get_channel(1191967326816444416).clone(name=(member.name+"'s voice channel"))
			member.move_to(new_channel)
		print(member)
		print(before)
		print(after)
		print("end")
		
		

async def setup(bot:commands.Bot):
	#  將Cog加入Bot中
	if(not enable):
		return
	await bot.add_cog(auto_vchannel(bot))
	print("[auto_vchannel] loaded")
