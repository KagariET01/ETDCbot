$v="beta"

echo "刪除舊image"
docker image rm -f discord_bot:$v
echo "建立image"
docker build -t discord_bot:$v -f ./Dockerfile ./
echo "刪除舊container"
docker container rm -f discord_bot_$v
echo "建立新container"
# docker run -d --name discord_bot_$v discord_bot:$v
docker run -it --name discord_bot_$v discord_bot:$v
# docker run -it --name discord_bot_beta discord_bot:beta
