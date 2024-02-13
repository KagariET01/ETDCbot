import json
import time
import datetime
import os

g_path=os.getenv("data_path")

data={}

def save():
	json.dump(data,open(g_path,"w+",encoding="utf-8"),ensure_ascii=False,sort_keys=True,allow_nan=True)
	print(f"\033[k[autosave]在{str(datetime.datetime.now())}已儲存")


def load():
	global data
	try:
		origdata=open(g_path,"r",encoding="utf-8")
		origdata=origdata.read()
		print("reading data.json\n",origdata)
		data=json.loads(origdata)
		print("[load]data.json載入成功")
	except:
		print("[load]data.json載入失敗")

def autosave():
	print("[autosave]已啟動自動儲存")
	nxt=datetime.datetime.now()+datetime.timedelta(minutes=1)
	while(1):
		if(datetime.datetime.now()>=nxt):
			nxt=datetime.datetime.now()+datetime.timedelta(minutes=1)
			save()
		else:
			time.sleep(1)
			pass

def showdata():
	print("[showdata]data.json內容：")
	print(json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True,allow_nan=True))



