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
import requests

BASE_URL = 'https://api.meraki.com/api/v1'


def get_Meraki_Organization(MERAKI_API_KEY):
	"""
	Get the Meraki Organizations that the API KEY has access to.
	:param MERAKI_API_KEY:
	:return:
	"""
	url = '{}/organizations'.format(BASE_URL)
	hdrs = {
		"Content-Type": "application/json",
    	"Accept": "application/json",
		"X-Cisco-Meraki-API-Key": MERAKI_API_KEY
	}

	response = requests.request('GET', url, headers=hdrs)
	return response.json()


def get_Meraki_Organization_Config_Changes(MERAKI_API_KEY, orgID, period):
	"""
	Get Meraki Organization configuration logs
	:param MERAKI_API_KEY:
	:param orgID:
	:param period:
	:return:
	"""
	final_Result = []
	seconds = int(period) * 60
	hdrs = {
		"Content-Type": "application/json",
		"Accept": "application/json",
		"X-Cisco-Meraki-API-Key": MERAKI_API_KEY
	}
	for org in orgID:
		url = '{}/organizations/{}/configurationChanges?timespan={}'.format(BASE_URL, org, seconds)
		response = requests.request('GET', url, headers=hdrs)
		result = response.json()
		for item in result:
			item['orgID'] = org
			final_Result.append(result)
	return final_Result
