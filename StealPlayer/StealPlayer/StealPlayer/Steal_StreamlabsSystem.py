import clr
import sys
import json
import os
import ctypes
import codecs

ScriptName = "Steal Player Minigame"
Website = "https://github.com/Ahnde/StreamLabsChatbot"
Description = "Steal Player Minigame for Streamlabs Bot"
Creator = "Ahnde"
Version = "1.0.0"

configFile = "config.json"
settings = {}

def Init():
	global settings

	path = os.path.dirname(__file__)
	try:
		with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
			settings = json.load(file, encoding='utf-8-sig')
	except:
		settings = {
			"liveOnly": True,
			"command": "!steal",
			"permission": "Everyone",
			"minAmount": 10,
			"maxAmount": 10000,
			"chance": 50,
			"useCooldown": True,
			"useCooldownMessages": True,
			"cooldown": 30,
			"onCooldown": "$user, $command is still on cooldown for $cd minutes!",
			"userCooldown": 180,
			"onUserCooldown": "$user $command is still on user cooldown for $cd minutes!",
			"responseWon": "$user stole $stealAmount $currency from $victim.",
			"responseLost": "$user couldn't steal any $currency and lost $stealAmount $currency to $victim.",
			"responsePointsNotInRange": "$user the amount for stealing needs to be between $minAmount and $maxAmount $currency.",
			"responseNotEnoughPoints": "$user, you need $stealAmount $currency to steal. It might go sideways!"
		}

def Execute(data):
	if data.IsChatMessage() and data.GetParam(0).lower() == settings["command"] and Parent.HasPermission(data.User, settings["permission"], "") and ((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"])):
		outputMessage = ""

		# Retrieve all user relevant data
		userId = data.User			
		userName = data.UserName
		userPoints = Parent.GetPoints(userId)

		# Retrieve the amount to steal
		stealAmountString = data.GetParam(2)
		if stealAmountString == '':
			stealAmount = settings['minAmount']
		else:
			stealAmount = int(stealAmountString)

		# Retrieve all victim relevant data
		victim = data.GetParam(1)
		victimId = GetUserIdForUserName(Parent, victim)
		if victimId == '':
			return
		victimName = Parent.GetDisplayName(victimId)
		victimPoints = Parent.GetPoints(victimId)

		# Check if the amount to steal is in bounds
		if stealAmount < settings["minAmount"] or settings["maxAmount"] < stealAmount:
			outputMessage = settings["responsePointsNotInRange"]
		# Check if the user has enough points to steal
		elif userPoints < stealAmount:
			outputMessage = settings["responseNotEnoughPoints"]
		# Check if any cooldown is activ
		elif settings["useCooldown"] and (Parent.IsOnCooldown(ScriptName, settings["command"]) or Parent.IsOnUserCooldown(ScriptName, settings["command"], userId)):
			if settings["useCooldownMessages"]:
				if Parent.GetCooldownDuration(ScriptName, settings["command"]) > Parent.GetUserCooldownDuration(ScriptName, settings["command"], userId):
					cdi = Parent.GetCooldownDuration(ScriptName, settings["command"])
					cd = str(cdi / 60) + ":" + str(cdi % 60).zfill(2) 
					outputMessage = settings["onCooldown"]
				else:
					cdi = Parent.GetUserCooldownDuration(ScriptName, settings["command"], userId)
					cd = str(cdi / 60) + ":" + str(cdi % 60).zfill(2) 
					outputMessage = settings["onUserCooldown"]
				outputMessage = outputMessage.replace("$cd", cd)
		# All checks went through - Steal coins
		else:
			if stealAmount > victimPoints:
				stealAmount = victimPoints
			
			if Parent.GetRandom(0, 101) <= settings["chance"]:
				Parent.RemovePoints(victimId, victimName, stealAmount)
				Parent.AddPoints(userId, userName, stealAmount)
				outputMessage = settings["responseWon"]
			else:
				Parent.RemovePoints(userId, userName, stealAmount)
				Parent.AddPoints(victimId, victimName, stealAmount)
				outputMessage = settings["responseLost"]

			if settings["useCooldown"]:
				Parent.AddUserCooldown(ScriptName, settings["command"], userId, settings["userCooldown"])
				Parent.AddCooldown(ScriptName, settings["command"], settings["cooldown"])

			newUserPoints = Parent.GetPoints(victimId)
			newVictimPoints = Parent.GetPoints(victimId)
			outputMessage = outputMessage.replace("$newUserPoints", str(newUserPoints))
			outputMessage = outputMessage.replace("$newVictimPoints", str(newVictimPoints))

		outputMessage = outputMessage.replace("$user", userName)
		outputMessage = outputMessage.replace("$victim", victimName)
		outputMessage = outputMessage.replace("$stealAmount", str(stealAmount))
		outputMessage = outputMessage.replace("$currency", Parent.GetCurrencyName())
		outputMessage = outputMessage.replace("$command", settings["command"])
		outputMessage = outputMessage.replace("$minAmount", str(settings["minAmount"]))
		outputMessage = outputMessage.replace("$maxAmount", str(settings["maxAmount"]))

		Parent.SendStreamMessage(outputMessage)
	return

def GetUserIdForUserName(Parent, user):
	userId = ''
	viewerList = Parent.GetViewerList()
	for viewer in viewerList:
		if Parent.GetDisplayName(viewer).lower() in user.lower():
			userId = viewer
	return userId

def OpenReadMe():
	location = os.path.join(os.path.dirname(__file__), "README.txt")
	os.startfile(location)
	return

def ScriptToggled(state):
	return

def ReloadSettings(jsonData):
	Init()
	return

def Tick():
	return
