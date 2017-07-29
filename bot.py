import discord, asyncio
import re

global player
player = []
client = discord.Client()

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	if not discord.opus.is_loaded():
		discord.opus.load_opus("opus.dll")
	if discord.opus.is_loaded():
		print('Opus ok')

@client.event
async def on_message(message):

	#AdminCommands
	if message.content.startswith('!nickname'):
		if str(message.author) == *adm*:
			await client.send_message(message.channel, 'something happened')
			name = re.sub(r'^!nickname ', '', message.content)
			client.change_nickname(client.user, name)
			
	if message.content.startswith('!add'):
		if str(message.author) == *adm*:
			temp = re.sub('^!add ', '', message.content)
			track = re.sub('@.*$', '', temp)
			src = re.sub('^.*@', '', temp)
			f = open('resources/yt_music.txt', 'a')
			f.write(track + '\n')
			f.write(src + '\n')
			f.close()
			await client.send_message(message.channel, 'Трек ' + track + ' добавлен в список!')
			
	if message.content.startswith('!comp'):
		if str(message.author) == *adm*:
			name = re.sub(r'^!comp ', '', message.content)
			for i in client.voice_clients:
				player.append (i.create_ffmpeg_player('music/' + name))
				player[-1].start()
				player[-1].volume = 0.2
	
	#Utility commands
	if re.search(r'^!помощь|^!help', message.content):
		file = open('help.txt', 'r')
		help = str(file.read())
		file.close		
		await client.send_message(message.channel, help)
		
	if re.search(r'^!пинг|^!ping', message.content):
		await client.send_message(message.channel, 'Понг!')
		
	if re.search(r'^ттс|^tts', message.content):
		msg = re.sub(r'^ттс |^tts ', '', message.content)
		await client.send_message(message.channel, msg, tts=True)
		
	if re.search(r'^!list', message.content):
		i = 0
		n = 0
		s = 'Вот все песни что я знаю:\n'
		f = open('resources/yt_music.txt', 'r')
		for line in f:
			if (i % 2 == 0):
				n = n + 1
				s = s + str(n) + ')' + line + '\n'
			i = i + 1
		f.close()
		await client.send_message(message.channel, s)
		
	#Dialogue commands
	if message.content.startswith('Привет, бот'):
		name = re.sub(r'#.*$', '', str(message.author))
		await client.send_message(message.channel, 'Привет, ' + name)
												
	#Music commands
	if message.content.startswith('!join'):
		vc = message.author.voice_channel
		voice = await client.join_voice_channel(vc)
		await client.send_message(message.channel, 'Я подключился к твоему чату!')
		
	if message.content.startswith('!leave'):
		for i in client.voice_clients:
			if (i.server == message.server):
				await i.disconnect()
		await client.send_message(message.channel, 'Меня больше нет в голосовых чатах этого сервера!')
	
	if message.content.startswith('!play'):
		for i in client.voice_clients:
			track = re.sub(r'!play ', '', message.content)
			await client.send_message(message.channel, 'Загружаю...')
			player.append (await i.create_ytdl_player(track))
			player[-1].start()
			player[-1].volume = 0.05
			await client.send_message(message.channel, 'Включаю \"' + str(player[-1].title))
			
	if message.content.startswith('!stop'):
		for i in player:
			i.stop()
		del player[:]
		await client.send_message(message.channel, 'Пластинка снята')
		
	if message.content.startswith('!pause'):
		for i in player:
			i.pause()
		await client.send_message(message.channel, 'Плеер на паузе')
		
	if message.content.startswith('!resume'):
		for i in player:
			i.resume()
		await client.send_message(message.channel, 'Возобновляю воспроизведение')
		
	if message.content.startswith('!volume'):
		vol = re.sub(r'!volume ', '', message.content)
		for i in player:
			i.volume = float(vol)
		await client.send_message(message.channel, 'Громкость изменена')
		
	if message.content.startswith('!run'):
		number = int(re.sub('^!run ', '', message.content))
		f = open('resources/yt_music.txt', 'r')
		for i in range (number):
			name = f.readline()
			src_file = f.readline()
		f.close()
		for j in client.voice_clients:
			await client.send_message(message.channel, 'Загружаю...')
			player.append (await j.create_ytdl_player(src_file))
			player[-1].start()
			player[-1].volume = 0.05
		await client.send_message(message.channel, 'Включаю ' + name)
		

client.run(*token*)
