#!/usr/bin/python3
import os
import requests
import json
import datetime
from requests.auth import HTTPBasicAuth

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

thousandeyes_user = os.environ['THOUSANDEYES_USER']
thousandeyes_token = os.environ['THOUSANDEYES_TOKEN']

url = "https://api.thousandeyes.com/v6/agents.json"

# Initialize the requests session
api_session = requests.Session()

response = api_session.request("GET", url, auth=HTTPBasicAuth(thousandeyes_user, thousandeyes_token), verify=False)

# If successfully able to get list of flows
if (response.status_code == 200):

    #agents = json.loads(response.content)
    #print(json.dumps(agentlists, indent=4))

    agents = json.loads(response.content)["agents"]
    for agent in agents:
        #print(json.dumps(flow, indent=4)) # formatted print
        if (agent['agentName'] == 'thousandeyes-va'):
            print(agent['agentState'])
            print(agent['lastSeen'])
# If unable to fetch list of alerts
else:
    print("An error has ocurred, while fetching agentlists, with the following code {}".format(response.status_code))

