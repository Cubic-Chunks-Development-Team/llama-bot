import discord
import asyncio
import json
import time
import threading

class UserEntry:

	def __init__(self, user_in):
		self.user = user_in
		self.cooldown = 0
		self.punishment = False
		self.heavyPunishment = False
		self.punishmentTimeLeft = 0


client = discord.Client()

token = ""

TIMEOUT_ROLE_ID = ""
TIMEOUT_CHANNEL_ID = ""
HEAVY_TIMEOUT_ROLE_ID = ""
SERVER_ID = ""

userdata = {}

def loadConfig():
	tfile = open("token.txt", "r")
	
	global token
	token = tfile.read()
	
	tfile.close()
	print(token)

	configfile = open("config.txt", "r")
	configtext =  configfile.read()
	configfile.close()

	confKVPairs = json.loads(configtext)
	
	global TIMEOUT_ROLE_ID
	global TIMEOUT_CHANNEL_ID
	global HEAVY_TIMEOUT_ROLE_ID
	global SERVER_ID
	
	TIMEOUT_ROLE_ID = confKVPairs["TIMEOUT_ROLE_ID"]
	TIMEOUT_CHANNEL_ID = confKVPairs["TIMEOUT_CHANNEL_ID"]
	HEAVY_TIMEOUT_ROLE_ID = confKVPairs["HEAVY_TIMEOUT_ROLE_ID"]
	SERVER_ID = str(confKVPairs["SERVER_ID"])

def setupRoles():
	global TIMEOUT_ROLE
	global HEAVY_TIMEOUT_ROLE
	global TIMEOUT_CHANNEL
	TIMEOUT_ROLE = discord.utils.find(lambda s: s.id == TIMEOUT_ROLE_ID, client.get_server(SERVER_ID).roles)
	HEAVY_TIMEOUT_ROLE = discord.utils.find(lambda s: s.id == HEAVY_TIMEOUT_ROLE_ID, client.get_server(SERVER_ID).roles)
	TIMEOUT_CHANNEL = client.get_channel(TIMEOUT_CHANNEL_ID)

@client.event
async def on_ready():
	setupRoles()
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------------')

@client.event
async def on_message(message):
	global TIMEOUT_ROLE_ID
	if message.author.bot:
		return
	if message.server.id == SERVER_ID:
		if (not (message.author.id in userdata)):
			userdata[message.author.id] = UserEntry(message.author)
		if (userdata[message.author.id].punishment):
			await client.send_message(TIMEOUT_CHANNEL, message.author.name + ", you still have " + str(userdata[message.author.id].punishmentTimeLeft) + " units of time left")
		userdata[message.author.id].cooldown += 15
		if (userdata[message.author.id].cooldown > 50):
			if (userdata[message.author.id].punishment):
				userdata[message.author.id].heavyPunishment = True
				await client.add_roles(message.author, HEAVY_TIMEOUT_ROLE)
			else:
				await client.send_message(message.channel, ":exclamation: :exclamation: :regional_indicator_s: :regional_indicator_p: :regional_indicator_a: :regional_indicator_m:     :regional_indicator_d: :regional_indicator_e: :regional_indicator_t: :regional_indicator_e: :regional_indicator_c: :regional_indicator_t: :regional_indicator_e: :regional_indicator_d: :exclamation: :exclamation:")
				await client.add_roles(message.author, TIMEOUT_ROLE)
				userdata[message.author.id].punishment = True
			userdata[message.author.id].punishmentTimeLeft = 450


async def doLoop():
	while True:
		await asyncio.sleep(0.1)
#		print("test")
		for u in userdata:
			if (userdata[u].cooldown > 0):
				userdata[u].cooldown -= 1
			userdata[u].punishmentTimeLeft -= 1
			if (userdata[u].punishmentTimeLeft == 0):
				if (userdata[u].heavyPunishment):
					userdata[u].heavyPunishment = False
					userdata[u].punishmentTimeLeft = 45
					await client.remove_roles(userdata[u].user, HEAVY_TIMEOUT_ROLE)
				else:
					userdata[u].punishment = False
					await client.remove_roles(userdata[u].user, TIMEOUT_ROLE)
				await client.send_message(TIMEOUT_CHANNEL, "End")
			elif (userdata[u].punishmentTimeLeft < 0):
				userdata[u].punishmentTimeLeft = 0

loadConfig()

#mainThread = threading.Thread(None, doLoop, "timingloop")
#mainThread.start()
loop = asyncio.get_event_loop()
# Blocking call which returns when the display_date() coroutine is done
loop.run_until_complete(asyncio.gather(doLoop(), client.start(token),))
loop.close()

client.run(token)



# Note: Code beyond this line was written in JavaScript and has not been ported.
'''
client.on("message", (message) => {
	if (message.author.bot)
		return;
	if (message.guild != null && message.guild.id == SERVER_ID) {

		if (message.content == "ping") {
			message.channel.send("Pong begin");
		// Usage!
		sleep(4000).then(() => {
			message.channel.send("Pong end");
		});
		
		}
	
	
		date = new Date();
		timerinfo = info[message.author.id];
		if (timerinfo == undefined)
			timerinfo = { lasttime: date.getTime(), totaltime: 0, punishment: false, completiontime: 0, heavypunishment: false }
		var t = date.getTime();
		timerinfo.totaltime += (2000 - (t - timerinfo.lasttime));
		timerinfo.lasttime = t;
		if (timerinfo.totaltime < 0) timerinfo.totaltime = 0;
		
		
		if (timerinfo.heavypunishment) {
			message.channel.send(message.author.username + ", you are muted.");
			message.delete();
			return;
		}
		
		if (timerinfo.punishment) {
			if (date.getTime() > timerinfo.completiontime) {
				message.member.removeRole(TIMEOUT_ROLE_ID, "SPAM");
				message.channel.send(message.author.username + ", I'm letting you go now.");
				timerinfo.punishment = false;
				message.member.setMute(false);
			} else {
				message.channel.send(message.author.username + ", you still have " + (0.001 * (timerinfo.completiontime - date.getTime())) + " seconds left in the time out corner.");
			}
		}
		
		if (timerinfo.totaltime > 8000) {
			timerinfo.totaltime = 0;
			message.channel.send(":exclamation: :exclamation: :regional_indicator_s: :regional_indicator_p: :regional_indicator_a: :regional_indicator_m:     :regional_indicator_d: :regional_indicator_e: :regional_indicator_t: :regional_indicator_e: :regional_indicator_c: :regional_indicator_t: :regional_indicator_e: :regional_indicator_d: :exclamation: :exclamation:");
			client.channels.get(TIMEOUT_CHANNEL_ID).send(":exclamation: :exclamation: :regional_indicator_s: :regional_indicator_p: :regional_indicator_a: :regional_indicator_m:     :regional_indicator_d: :regional_indicator_e: :regional_indicator_t: :regional_indicator_e: :regional_indicator_c: :regional_indicator_t: :regional_indicator_e: :regional_indicator_d: :exclamation: :exclamation:");
			
			if (timerinfo.punishment) {
				client.channels.get(TIMEOUT_CHANNEL_ID).send(message.author.username + ", I can't believe this. Spamming in the thinking corner? I'l sorry to say I'll have to mute you.");
				
				sleep(2000).then(() => {
					message.member.addRole(HEAVY_TIMEOUT_ROLE_ID, "SPAM");
				});
				
				timerinfo.heavypunishment = true;
				info[message.author.id] = timerinfo;
				sleep(90000).then(() => {
					timerinfo.heavypunishment = false;
					message.member.removeRole(HEAVY_TIMEOUT_ROLE_ID, "SPAM");
					client.channels.get(TIMEOUT_CHANNEL_ID).send(message.author.username + ", I've unmuted you, but you still need to be in the timeout corner a bit.");
					timerinfo.completiontime = date.getTime() + 45000;
					timerinfo.punishment = true;
					info[message.author.id] = timerinfo;
					message.member.addRole(TIMEOUT_ROLE_ID, "SPAM");
				});
			}
			else {
				client.channels.get(TIMEOUT_CHANNEL_ID).send(message.author.username + ", you have spammed too much. You need to go think about your actions a bit.");
			}
			timerinfo.completiontime = date.getTime() + 45000;
			
			timerinfo.punishment = true;
			sleep(2000).then(() => {
				message.member.addRole(TIMEOUT_ROLE_ID, "SPAM");
			});
		}
		info[message.author.id] = timerinfo;
	} else if (message.channel instanceof Discord.DMChannel) {
		if (message.channel.recipient.id == "125612588271665152") {
			client.channels.get("331900978548965376").send(message.content);
		}
	}
});
'''