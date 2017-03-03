import aiml
import os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
from datetime import date

chatBot = aiml.Kernel()

#if os.path.isfile("bot_brain.brn"):
#    chatBot.bootstrap(brainFile = "bot_brain.brn")
#else:
chatBot.bootstrap(learnFiles = "std-startup.xml", commands = "load aiml b")
chatBot.saveBrain("bot_brain.brn")

print "\n"
print chatBot.respond("Init")

goalList = [ "awareness" , "conversion" , "sale" ]
typeList = [ "display" , "search" ]

undefined_values = 8

campaign_id = -1
ad_groups = "undefined"
campaignName = "undefined"
campaignGoal = "undefined"
campaignType = "undefined"
dateDebut = "undefined"
dateFin = "undefined"
campaignBudget = -1

bot_response=""

# chatBot now ready for use
while True:
	message = raw_input("\nYour message: ")
	if message == "quit":
		exit()
	elif message == "brain":
		chatBot.saveBrain("bot_brain.brn")
	elif message == "save":
		#fill a line in CampaignSheet CSV
		with open('campaignsheet.csv', 'ab') as csvfile:
		    fieldnames = ['campaign_id', 'ad_groups','campaignName','campaignGoal','campaignType','dateDebut','dateFin','campaignBudget']
		    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		    writer.writerow({'campaign_id':campaign_id, 'ad_groups':ad_groups,'campaignName':campaignName,'campaignGoal':campaignGoal,'campaignType':campaignType,'dateDebut':dateDebut,'dateFin':dateFin,'campaignBudget':campaignBudget})
	else:
		bot_response = chatBot.respond(message)

		# Nom de Campagne
		if bot_response.startswith('Your campaign is called'):
			if campaignName == "undefined":
				undefined_values = undefined_values - 1
			campaignName = bot_response[24:]
			# Test sur le stockage du nom de campagne
			#print "-" + campaignName + "-" + str(undefined_values) + "-"
			# Reponse du chatBot
			print "\n" + bot_response
			# Envoi vers la prochaine etape
			print chatBot.respond('Budget')

		# Changement nom de campagne
		elif bot_response.startswith('Your campaign is now called'):
			if campaignName == "undefined":
				undefined_values = undefined_values - 1
			campaignName = bot_response[28:]
			# Test sur le stockage du nom de campagne
			#print "-" + campaignName + "-" + str(undefined_values) + "-"
			# Reponse du chatBot
			print "\n" + bot_response

		# Budget de la Campagne
		elif bot_response.startswith('Your budget is '):
			if campaignBudget == -1:
				undefined_values = undefined_values - 1
			campaignBudget = bot_response[15:-8]
			## Verifier si il s'agit bien dun nombre

			#print "-" + campaignBudget + "-" + str(undefined_values) + "-"
			print "\n" + bot_response
			print chatBot.respond('Goal')

		# But de la Campagne
		elif bot_response.startswith('Your goal is '):
			if bot_response[13:] in goalList:
				if campaignGoal == "undefined":
					undefined_values = undefined_values - 1
				campaignGoal = bot_response[13:]
				#print "-" + campaignGoal + "-" + str(undefined_values) + "-"
				print "\n" + bot_response
				print chatBot.respond('Type')
			else:
				print "I did not understand"
				print chatBot.respond('Goal')

		# Type de Campagne
		elif bot_response.endswith(' sounds good to me'):
			#print "-" + bot_response[2:-27] + "-" 
			if bot_response[2:-27] in typeList:
				if campaignType == "undefined":
					undefined_values = undefined_values - 1
				campaignType = bot_response[2:-27]
				#print "-" + campaignType + "-" + str(undefined_values) + "-"
				print "\n" + bot_response
				print chatBot.respond('Start Date')
			else:
				print "I did not understand"
				print chatBot.respond('Type')

		# Debut de la Campagne
		elif bot_response.startswith('We will start on '):
			if dateDebut == "undefined":
					undefined_values = undefined_values - 1
			# Date au format ddmmyyyy
			dateDebut = bot_response[17:19] + '/' + bot_response[19:21] + '/' + bot_response[21:25]
			#print "-" + dateDebut + "-" + str(undefined_values) + "-"
			print "\n" + bot_response
			print chatBot.respond('End Date')

		# Fin de la Campagne
		elif bot_response.startswith('We will end the'):
			if dateFin == "undefined":
					undefined_values = undefined_values - 1
			# Date au format ddmmyyyy
			dateFin = bot_response[28:30] + '/' + bot_response[30:32] + '/' + bot_response[32:37]
			#print "-" + dateFin + "-" + str(undefined_values) + "-"
			print "\n" + bot_response

		# Resultats de la campagne
		elif bot_response.startswith('Results'):
			print "\n" + bot_response
			ad_results = pd.read_csv('ad_results.csv', sep=';', encoding='latin1', parse_dates=[['date','heure']],dayfirst=True)
			sum_impressions = pd.pivot_table(data=ad_results, index='ad_id', values=['impressions'],aggfunc=[np.sum, np.mean, np.min,np.max])
			sum_impressions.columns = sum_impressions.columns.get_level_values(0)
			impressions_ad1 = sum_impressions['sum'][1]
			impressions_ad2 = sum_impressions['sum'][2]

			for i in list(ad_results['ad_id'].unique()):
			    print 'La pub avec l ad ID ' + str(i) + " a genere " + str(sum_impressions['sum'][i]) + " impressions sur la periode"

			if impressions_ad2 > impressions_ad1:
			    print "La pub 2 a genere plus d'impressions que la pub 1"
			else:
			    print "La pub 1 performe mieux que la pub 2"

		else:
			print "\n" + bot_response
			# Do something with bot_response