import aiml
import os

chatBot = aiml.Kernel()

#if os.path.isfile("bot_brain.brn"):
#    chatBot.bootstrap(brainFile = "bot_brain.brn")
#else:
chatBot.bootstrap(learnFiles = "std-startup.xml", commands = "load aiml b")
chatBot.saveBrain("bot_brain.brn")

print (n)
print chatBot.respond("Init")

goalList = [ "awareness" , "conversion" , "sale" ]
typeList = [ "display" , "search" ]

bot_response=""

# chatBot now ready for use
while True:
	message = raw_input("\nYour message: ")
	if message == "quit":
		exit()
	elif message == "save":
		chatBot.saveBrain("bot_brain.brn")
	elif message == "test":
		print campaignName
	else:
		bot_response = chatBot.respond(message)

		# Recuperation du nom de campagne
		if bot_response.startswith('Your campaign is now called'):
			campaignName = bot_response[28:]
			# Test sur le stockage du nom de campagne
			print campaignName 
			# Reponse du chatBot
			print n + bot_response
			# Envoi vers la prochaine etape
			print chatBot.respond('Budget')
		elif bot_response.startswith('Your budget is '):
			campaignBudget = bot_response[15:-8]
			## Verifier si il s'agit bien dun nombre

			print ("-" + campaignBudget + "-")
			print n + bot_response
			print chatBot.respond('Goal')
		elif bot_response.startswith('Your goal is '):
			campaignGoal = bot_response[13:]
			print "-" + campaignGoal + "-"
			if campaignGoal in goalList:
				print n + bot_response
				print chatBot.respond('Type')
			else:
				print "I did not understand"
				print chatBot.respond('Goal')
		elif bot_response.endswith(' sounds good to me'):
			campaignType = bot_response[2:-18]
			print "-" + campaignType + "-"
			if campaignType in typeList:
				print n + bot_response
				print chatBot.respond('Start Date')
			else:
				print "I did not understand"
				print chatBot.respond('Type')
		elif bot_response.startswith('We will start on '):
			# Date au format ddmmyyyy
			dateDebut = bot_response[17:25]
			print "-" + dateDebut + "-"
			print n + bot_response
			
		else:
			print n + bot_response
			# Do something with bot_response