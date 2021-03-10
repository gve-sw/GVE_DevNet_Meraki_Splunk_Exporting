"""
Copyright (c) 2021 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""
import pandas
import schedule
import time
import merakiAPI


def automated_Behaviour(MERAKI_API_KEY, orgID, period):
	"""
	Automated behaviour of the script
	:param MERAKI_API_KEY:
	:param orgID:
	:return:
	"""
	t = time.localtime()
	current_time = time.strftime("%d-%m-%y %H:%M:%S", t)
	print("Retrieving Meraki Org Config Changes -- {}".format(current_time))
	log_Output_List = merakiAPI.get_Meraki_Organization_Config_Changes(MERAKI_API_KEY, orgID, period)
	if log_Output_List == []:
		print('No Organization Config Changes found...')
	for log_Output in log_Output_List:
		log_Output_DF = pandas.DataFrame(log_Output)
		log_Output_DF.to_csv('Configuration_Logs/{}.csv'.format(current_time), mode='a')
		print("Config Changes stored!")


# SCRIPT
schedule.clear()
print('STARTING MERAKI CONFIG EXPORT...')
print('--------------------------------')
apiKey = input('Please provide a valid Meraki API Key: ')
org_Json = merakiAPI.get_Meraki_Organization(apiKey)
print('Organizations Found:')
for org in org_Json:
	print('--- {}'.format(org['name']))
print('--- all')
orgName = input('Enter Meraki Organization to log: ')
period = input('How often would you like to poll for config changes? (in minutes): ')
orgID = []
for org in org_Json:
	if orgName == 'all':
		orgID.append(org['id'])
	else:
		if orgName == org['name']:
			orgID.append(org['id'])
if int(period) == 1:
	schedule.every(int(period)).minute.do(automated_Behaviour, orgID=orgID, MERAKI_API_KEY=apiKey, period=period)
else:
	schedule.every(int(period)).minutes.do(automated_Behaviour, orgID=orgID, MERAKI_API_KEY=apiKey, period=period)
print('Job Scheduled!')

while True:
	schedule.run_pending()
	time.sleep(10)

