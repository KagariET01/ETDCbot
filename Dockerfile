


FROM dc_py:latest

WORKDIR /app

COPY ./ $WORKDIR


ENV DCtoken="你的機器人token"
# 機器人的token可以在 https://discord.com/developers/applications/應用程式id/bot中找到
ENV DCwebhook="用來傳送日誌的webhook連結，不想設定就留白"
ENV logchannel="webhook會傳送過去的頻道id，沒設定webhook或不會取得頻道id就留白（連同webhook都要留白，避免發生連鎖效應）"



ENV adminid="你的discord id，你將雍有所有的控制權（也就是皇帝）"
ENV data_path="./data.json"
ENV timezone=8
#  data_path是資料庫的位置，預設是在根目錄下的data.json，可以自行更改
#  除非有特殊需求，否則不建議更改

RUN echo "{}" > ${data_path}

CMD python3 main.py

