# ETDCbot

就...KagariET01做的機器人  
目前正執行饅頭機器人搬運計畫  

# 事前準備

## 申請Discord Bot Token

這裡只概述如何建立新的機器人，詳細教學可以看[這裡](https://github.com/KagariET01/DCbot_note)  
若已經會申請DC Token，可略過此步驟，直接跳到[建立Debug頻道](#建立Debug頻道)

1. 註冊（或登入）[Discord][Discord]帳號
1. 進入到[Discord Dev][Discord Dev]管理頁面
1. 點擊右上角的 `New Application` 來建立新的應用程式
1. 左側點擊 `Bot` 進入機器人設定頁面
1. 下面的 `PRESENCE INTENT` `SERVER MEMBERS INTENT` `MESSAGE CONTENT INTENT` 都勾起來，來授權你的機器人可以收發訊息或做其他事情
1. 最重要的：點擊 `Reset Token` ，待會要用到這個Token，先記錄起來
	- 此Token相當於帳號密碼，不可外洩給其他人
1. 點擊左側的 `OAuth2` > `URL Generator` 來取得機器人的授權連結
1. `bot` 選項打勾，此時你會在下方看到更多機器人的權限選項  
	- 這些權限是版主加入機器人時會有的權限，可***依個人需求勾選***
		- 不管到哪裡，你的機器人都會有這些權限，除非管理員另外設定
	- 當然，***可以都不勾***，此時機器人將不要求任何權限
		- 機器人預設可獲得 `@everyone` 的權限
		- 機器人的其他權限管理可以透過身分組調整
		- 簡單來說：把機器人當一般用戶管理即可
1. 最下面會產生一個超連結，版主使用這個連結就可以把機器人加到自己的伺服器

## 建立Debug頻道

p.s. 此部分並非強制設定，此部分是為了方便機器人的開發者除錯用的  
若不想設定，可直接跳到[使用方法](#使用方法)

1. 建立一個文字頻道，此頻道最好只有你（和維護團隊），因為它會發送一些敏感資訊，不可外洩
1. 將該頻道的通知關閉（因為會很吵）
1. 右鍵頻道>編輯頻道>整合>Webhook>新Webhook>複製Webhook網址
1. 這個Webhook網址會用來發送Debug資訊，待會會用到，先記錄起來
	- 此Webhook網址不可外洩，不然會有騷擾、惡意訊息攻擊
1. 右鍵頻道>複製頻道ID，這個ID待會會用到，先記錄起來
	- 此ID是為了確保機器人不會監聽到Debug資訊而導致無限遞迴

# 使用方法

本機器人提供兩種使用方法：

1. Docker
2. 直接使用指令

p.s. 無論是哪種方法，此教學都是針對Linux撰寫的，其他作業系統所使用的指令會稍有不同

## 先把原始碼下載下來

way 1. 使用git
```bash
git clone git@github.com:KagariET01/ETDCbot.git
```
way 2. 下載.zip包，到[這裡][rp]>Code>Download ZIP下載壓縮包

## Docker

若你操控遠端伺服器、想增加DC bot的穩定度，或單純覺得旁邊開著終端機很礙眼，可以考慮使用Docker  
此安裝方法涉及到Docker的基礎知識，若對Docker不熟悉，可以考慮用指令架設  

1. 安裝Docker  
	```bash
	sudo apt-get update
	sudo apt-get install docker
	```
1. 我們要先建立一個包含Python環境的Docker Image
	```bash
	sh pydc/build.sh #建立包含Python環境的Docker Image
	```
1. 修改[Dockerfile][Dockerfile]  
	1. 修改`ENV DCtoken`成你的Discord Bot Token
	1. 修改`ENV DCwebhook`成你的Debug頻道Webhook網址
	1. 修改`ENV logchannel`成你的Debug頻道ID
	1. 修改`ENV adminid`成你的Discord ID
		- 這將授予該用戶超級權限，可操控機器人
		- 獲取方法：左下角>點自己的帳號>複製使用者ID
	1. 修改完後，他應該會長得像[Dockerfile_ex](./Dockerfile_ex)
		- p.s. 該檔案裡的設定都是亂打的，如有雷同純屬巧合
1. 執行`build.sh`，此指令會自動部屬虛擬機，並執行機器人
1. 若要重新啟動，可執行下列指令
	```bash
	docker stop discord_bot_beta #  關閉Docker container
	docker start discord_bot_beta #  啟動Docker container
	```



## 使用指令

1. 先安裝Python3以及其他插件
	p.s. requirements.txt在pydc目錄下面，而非根目錄
	```bash
	sudo apt-get update
	sudo apt-get install python3 python3-pip
	pip3 install -r pydc/requirements.txt
	```
1. 先執行下列指令來設定環境變數（此設定會在終端機關閉後失效）
	```bash
	export DCtoken=<你的Discord Bot Token>
	export DCwebhook=<你的Debug頻道Webhook網址>
	export logchannel=<你的Debug頻道ID>
	export adminid=<你的Discord ID>
	export data_path="./data.json"
	```
	- 修改完後，他應該會長這樣  
		```bash
		export DCtoken=MTIwwxxxxxxxxxxxxxxxxxxxxxxxxxx
		export DCwebhook=https://discord.com/api/webhooks/1200782469830561892/zDexxxxxxxxxxxxxxxxxxxxxx
		export logchannel=123456789123456789123456789
		export adminid=123456789123456789
		export data_path="./data.json"
		```
	- 重啟機器人可能需要重打這些指令，可以另存個.sh檔
1. 我們要建立空的資料庫，執行下列指令
	```bash
	echo "{}" > $data_path
	```
1. 執行機器人
	```bash
	python3 main.py
	```
1. 若要重新啟動，請按`Ctrl+C`停止機器人，然後再執行`python3 main.py`
	- 若你關閉終端機，你可能要重新設定環境變數

# 更新

更新分為兩個版本：Docker和純指令

## 先匯出資料

1. 登入Discord，並進入有機器人的頻道
1. 在聊天室輸入`/save`
1. 在聊天室輸入`/export`
1. 機器人會將資料以Json格式傳送給你

## Docker

1. 將[Dockerfile][Dockerfile]複製出來，它裡面有你的機器人設定
1. 使用以下指令，下載最新的原始碼
	```bash
	git pull
	```
1. 將[Dockerfile][Dockerfile]覆蓋過去
1. 載次執行`build.sh`，此指令會自動部屬虛擬機，並執行機器人

## 使用指令

1. 先使用`Ctrl+C`停止機器人
1. 使用以下指令，下載最新的原始碼
	```bash
	git pull
	```
1. 執行機器人
	```bash
	python3 main.py
	```

## 別忘了回復資料

1. 在你和機器人的私訊中，輸入`/recovery dta=<剛剛的json資料>`來回復設定
1. 在同樣的地方輸入`/reload`，讓機器人重新載入資料



# 目前支援的指令

- `two_fan.py` 二番賞
	- `/2fan_r`  `lst  (清單)`  建立新的二番賞
		- p.s. 每個server只能有一個二番賞
		- 越左邊的獎項越高級
		- 獎項分為1等獎到n等獎
			- ~~為何不是A到Z呢，因為這是二番賞~~
		- 清單格式範例如下
			- 不同元素之間以逗點  `,`  分隔
				```txt
				1,2,3,4,5
				```
				代表有一個一等獎、兩個二等獎...五個五等獎
	- `/2fan_see` 查看還沒被抽走的號碼
	- `/2fan_get`  `id  (int)` 抽獎
		- 老闆會告訴你該編號的籤是什麼獎

- `which.py` 哪個
	- `哪個 ` `清單`
		- 隨機回傳清單裡的東西
		- 清單以空格分隔
		- 標準格式範例如下
			```txt
			哪個 小ㄌㄌ 大美女 小正太 大帥哥
			```

- `help.py` help
	- `/help`
		- 就是字面上的意思

- `tf.py`  是不是、要不要、有沒有
	- ...`是不是`...
	- ...`要不要`...
	- ...`有沒有`...
	- 隨機回復  `是` 、 `不是` ......

- `random.py` 隨機取數
	- `/random`  `l (int) = 1`  `r (int) = 100`  
		- 在l~r之間隨機取一亂數

- `pet.py` 迷你寵物
	- 提及該機器人，機器人可能會有一些反應
	- 這邊有一些例子
		- @ bot 早安
		- @ bot 午安
		- @ bot 晚安
		- @ bot 宵夜安
		- @ bot 零晟安
		- @ bot 清晟安
		- @ bot 起床安
		- @ bot XXXX（自己猜）





# LICENSE 版權許可

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/KagariET01/ETDCbot">ETDCbot</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://kagariet01.github.io/about">KagariET01</a> is licensed under <a href="http://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY-NC-SA 4.0<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1"></a></p>

[Dockerfile]:./Dockerfile
[Discord]:https://discord.com/register?redirect_to=%2Fdevelopers%2Fapplications
[Discord Dev]:https://discord.com/developers/applications
[rp]:https://github.com/KagariET01/ETDCbot
