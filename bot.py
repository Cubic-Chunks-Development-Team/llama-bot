import discord
import asyncio
import json
import time
import configparser
import math

class UserEntry:
	def __init__(self, user_in):
		self.user = user_in
		self.cooldown = 0
		self.slowcooldown = 0
		self.punishment = False
		self.heavyPunishment = False
		self.punishmentTimeLeft = 0

class Quote:
	def __init__(self, text_in, author_in, timestamp_in):
		self.text = text_in
		self.author = author_in
		self.timestamp = timestamp_in

client = discord.Client()

token = ""

TIMEOUT_ROLE_ID = ""
TIMEOUT_CHANNEL_ID = ""
HEAVY_TIMEOUT_ROLE_ID = ""
SERVER_ID = ""
TIMEOUT_BYPASS_ROLE_ID = ""

TimeoutDuration = 0
HeavyTimeoutDuration = 0
NewlineWeight = 0
CharacterWeight = 0
FastTimerMultiplier = 0
FastTimerThreshold = 0
SlowTimerMultiplier = 0
SlowTimerThreshold = 0


userdata = {}

def getFormattedMessage(id, *args):
	return config["lang"][id] % args

def loadConfig():
	tfile = open("token.txt", "r")
	
	global token
	token = tfile.read()
	tfile.close()
	print(token)

	global config
	config = configparser.ConfigParser()
	config.read("config.txt")
	
	global TIMEOUT_ROLE_ID
	global TIMEOUT_CHANNEL_ID
	global HEAVY_TIMEOUT_ROLE_ID
	global SERVER_ID
	global TIMEOUT_BYPASS_ROLE_ID
	
	TIMEOUT_ROLE_ID = config["llama-bot"]["TIMEOUT_ROLE_ID"]
	TIMEOUT_CHANNEL_ID = config["llama-bot"]["TIMEOUT_CHANNEL_ID"]
	HEAVY_TIMEOUT_ROLE_ID = config["llama-bot"]["HEAVY_TIMEOUT_ROLE_ID"]
	SERVER_ID = config["llama-bot"]["SERVER_ID"]
	TIMOUT_BYPASS_ROLE_ID = config["llama-bot"]["TIMEOUT_BYPASS_ROLE_ID"]
	
	global TimeoutDuration
	global HeavyTimeoutDuration
	global NewlineWeight
	global CharacterWeight
	global FastTimerMultiplier
	global FastTimerThreshold
	global SlowTimerMultiplier
	global SlowTimerThreshold
	
	TimeoutDuration = int(config["llama-bot"]["TimeoutDuration"])
	HeavyTimeoutDuration = int(config["llama-bot"]["HeavyTimeoutDuration"])
	NewlineWeight = float(config["llama-bot"]["NewlineWeight"])
	CharacterWeight = float(config["llama-bot"]["CharacterWeight"])
	FastTimerMultiplier = int(config["llama-bot"]["FastTimerMultiplier"])
	FastTimerThreshold = int(config["llama-bot"]["FastTimerThreshold"])
	SlowTimerMultiplier = int(config["llama-bot"]["SlowTimerMultiplier"])
	SlowTimerThreshold = int(config["llama-bot"]["SlowTimerThreshold"])

def setupRoles():
	global TIMEOUT_ROLE
	global HEAVY_TIMEOUT_ROLE
	global TIMEOUT_CHANNEL
	global TIMEOUT_BYPASS_ROLE
	TIMEOUT_ROLE = discord.utils.find(lambda s: s.id == TIMEOUT_ROLE_ID, client.get_server(SERVER_ID).roles)
	HEAVY_TIMEOUT_ROLE = discord.utils.find(lambda s: s.id == HEAVY_TIMEOUT_ROLE_ID, client.get_server(SERVER_ID).roles)
	TIMEOUT_CHANNEL = client.get_channel(TIMEOUT_CHANNEL_ID)
	TIMEOUT_BYPASS_ROLE = discord.utils.find(lambda s: s.id == TIMEOUT_BYPASS_ROLE_ID, client.get_server(SERVER_ID).roles)

@client.event
async def on_ready():
	setupRoles()
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------------')

@client.event
async def on_message(message):

	if message.author.bot:
		return

	if message.server.id == SERVER_ID:

		if (message.content.startswith("$")):
			args = message.content.split(" ")
			if (args[0] == "$ping"):
				await client.send_message(message.channel, "pong")
			if (args[0] == "$quote"):
				await client.send_message(message.channel, "todo")
			return
				
		if not (TIMEOUT_BYPASS_ROLE is None) and TIMEOUT_BYPASS_ROLE in message.author.roles:
			return
			
		if (not (message.author.id in userdata)):
			userdata[message.author.id] = UserEntry(message.author)
			
		if (userdata[message.author.id].punishment):
			await client.send_message(TIMEOUT_CHANNEL, getFormattedMessage("PunishmentTime", message.author.name, userdata[message.author.id].punishmentTimeLeft*0.1))
			
		lines = message.content.count("\n")
		score = (lines * NewlineWeight + len(message.content) * CharacterWeight) + 1.0
		userdata[message.author.id].cooldown += (FastTimerMultiplier * score)
		userdata[message.author.id].slowcooldown += (SlowTimerMultiplier * score)
			
		if (userdata[message.author.id].cooldown > FastTimerThreshold or userdata[message.author.id].slowcooldown > SlowTimerThreshold):
			
			if (userdata[message.author.id].punishment):
				userdata[message.author.id].heavyPunishment = True
				await client.add_roles(message.author, HEAVY_TIMEOUT_ROLE)
				await client.send_message(TIMEOUT_CHANNEL, getFormattedMessage("HeavyPunishmentStart", message.author.name))
				userdata[message.author.id].punishmentTimeLeft = HeavyTimeoutDuration * 10
				
			else:
				await client.send_message(message.channel, getFormattedMessage("SpamAlert"))
				await client.add_roles(message.author, TIMEOUT_ROLE)
				userdata[message.author.id].punishment = True
				await client.send_message(TIMEOUT_CHANNEL, getFormattedMessage("PunishmentStart", message.author.name))
				userdata[message.author.id].punishmentTimeLeft = TimeoutDuration * 10
				
			userdata[message.author.id].cooldown = 0
			userdata[message.author.id].slowcooldown = 0


async def doLoop():

	while True:

		await asyncio.sleep(0.1)
		for u in userdata.copy():

			if (userdata[u].cooldown > 0):
				userdata[u].cooldown -= 1
			if (userdata[u].slowcooldown > 0):
				userdata[u].slowcooldown -= 1
				
			userdata[u].punishmentTimeLeft -= 1
				
			if (userdata[u].punishmentTimeLeft == 0):
				
				if (userdata[u].heavyPunishment):
					userdata[u].heavyPunishment = False
					userdata[u].punishmentTimeLeft = TimeoutDuration * 10
					await client.remove_roles(userdata[u].user, HEAVY_TIMEOUT_ROLE)
					await client.send_message(TIMEOUT_CHANNEL, getFormattedMessage("HeavyPunishmentEnd", userdata[u].user.name))
					
				else:
					userdata[u].punishment = False
					await client.remove_roles(userdata[u].user, TIMEOUT_ROLE)
					await client.send_message(TIMEOUT_CHANNEL, getFormattedMessage("PunishmentEnd", userdata[u].user.name))
					
			elif (userdata[u].punishmentTimeLeft < 0):
				userdata[u].punishmentTimeLeft = 0


loadConfig()
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(doLoop(), client.start(token)))
loop.close()
client.run(token)
