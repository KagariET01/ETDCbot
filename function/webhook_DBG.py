import discord
import discord.ext

import requests
import json
import os

hook=os.getenv("DCwebhook")

def send_DC(txt,bef="",aft=""):#  將訊息傳送到DC
	print(bef+str(txt)+aft)
	# hook=os.getenv("DCwebhook")
	data={
		"content":("```txt\n"+txt+"\n```"),
		"username":"小ㄌㄌ",
		"avatar_url":"https://avatars.githubusercontent.com/u/66681962",
		"attachments":[]
	}
	if(hook==None or hook==""):
		print("未設定DCwebhook")
		return
	if(hook==""):
		print("未設定DCwebhook")
		return
	r=requests.post(hook,json.dumps(data),headers={'Content-Type':'application/json'})

def get_msn(message:discord.Message):#  監聽訊息
	# hook=os.getenv("DCwebhook")
	eb=[]
	if(1):#  伺服器
		try:
			eb.append(
				{
					"title":"伺服器",
					"color":16711680,
					"fields":[
						{"name":"伺服器名稱","value":str(message.guild.name),"inline":True},
						{"name":"伺服器ID","value":str(message.guild.id),"inline":True},
					],
					"footer": {
						"text": "BOT by ET01"
					}
				}
			)
		except:
			eb.append(
				{
					"title":"伺服器",
					"color":16711680,
					"fields":[
						{"name":"NOT FOUND","value":"NOT FOUND","inline":True},
					],
					"footer": {
						"text": "BOT by ET01"
					}
				}
			)

	if(1):#  頻道
		try:
			eb.append(
				{
					"title":"頻道",
					"color":16711680,
					"fields":[
						{"name":"頻道名稱","value":str(message.channel.name),"inline":True},
						{"name":"頻道ID","value":str(message.channel.id),"inline":True},
						{"name":"頻道人數","value":str(len(message.channel.members)),"inline":True},
					],
					"footer": {
						"text": "BOT by ET01"
					}
				}
			)
		except:
			eb.append(
				{
					"title":"頻道",
					"color":16711680,
					"fields":[
						{"name":"NOT FOUND","value":"NOT FOUND","inline":True},
					],
					"footer": {
						"text": "BOT by ET01"
					}
				}
			)

	if(1):#  傳訊者
		try:
			eb.append(
				{
					"title":"傳訊者",
					"color":16711680,
					"fields":[
						{"name":"傳訊者名稱（可用來加友","value":str(message.author.name),"inline":True},
						{"name":"傳訊者伺服器暱稱","value":str(message.author.nick),"inline":True},
						{"name":"傳訊者名稱","value":str(message.author.global_name),"inline":True},
						{"name":"傳訊者ID","value":str(message.author.id),"inline":True},
					],
					"footer": {
						"text": "BOT by ET01"
					}
				},
			)
		except:
			eb.append(
				{
					"title":"傳訊者",
					"color":16711680,
					"fields":[
						{"name":"NOT FOUND","value":"NOT FOUND","inline":True},
					],
					"footer": {
						"text": "BOT by ET01"
					}
				}
			)

	if(1):#  回復向
		try:
			eb.append(
				{
					"title":"回復向...",
					"color":16711680,
					"fields":[
						{"name":"回覆ID","value":str(message.reference.message_id),"inline":True},
						{"name":"回覆內容","value":str(message.reference.resolved.content),"inline":True},
					],
					"footer": {
						"text": "BOT by ET01"
					}
				},
			)
		except:
			eb.append(
				{
					"title":"回復向...",
					"color":16711680,
					"fields":[
						{"name":"NOT FOUND","value":"NOT FOUND","inline":True},
					],
					"footer": {
						"text": "BOT by ET01"
					}
				}
			)

	if(1):#  訊息
		try:
			eb.append(
				{
					"title":"訊息",
					"color":16711680,
					"fields":[
						{"name":"訊息ID","value":str(message.id),"inline":True},
						{"name":"訊息內容","value":str(message.content),"inline":True},
					],
					"footer": {
						"text": "BOT by ET01"
					}
				},
			)
		except:
			eb.append(
				{
					"title":"訊息",
					"color":16711680,
					"fields":[
						{"name":"NOT FOUND","value":"NOT FOUND","inline":True},
					],
					"footer": {
						"text": "BOT by ET01"
					}
				}
			)

	if(eb==[]):#  空白
		eb.append(
			{
				"title":"NOT FOUND","value":"NOT FOUND","inline":True,
				"color":16711680,
				"fields":[
					{"name":"NOT FOUND","value":"NOT FOUND","inline":True},
				],
				"footer": {
					"text": "BOT by ET01"
				}
			}
		)
	
	data={#  建立傳送資料
		# "content":"",
		"username":"小ㄌㄌ",
		"avatar_url":"https://avatars.githubusercontent.com/u/66681962",
		"attachments":[],
		"embeds":eb
	}
	
	if(hook==""):
		print("未設定DCwebhook")
		return
	r=requests.post(hook,json.dumps(data),headers={'Content-Type':'application/json'})
	# print("[dishook][get_msn]已傳送訊息\n",data)

def get_user(user:discord.User):#  獲取使用者資料
	# hook=os.getenv("DCwebhook")
	data={
		# "content":"",
		"username":"小ㄌㄌ",
		"avatar_url":"https://avatars.githubusercontent.com/u/66681962",
		"attachments":[],
		"embeds":[
			{
				"title":"使用者",
				"color":16711680,
				"fields":[
					{"name":"傳訊者名稱（可用來加友","value":str(user.name),"inline":True},
					{"name":"傳訊者名稱","value":str(user.global_name),"inline":True},
					{"name":"傳訊者ID","value":str(user.id),"inline":True},
				],
				"footer": {
					"text": "BOT by ET01"
				}
			}
		]
	}
	
	if(hook==""):
		print("未設定DCwebhook")
		return
	r=requests.post(hook,json.dumps(data),headers={'Content-Type':'application/json'})


if(__name__=="__main__"):
	send_DC(input("輸入要傳送的訊息："))