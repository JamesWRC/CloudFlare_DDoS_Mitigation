#!/usr/bin/env python3

import json
import requests
import sqlalchemy
from apiConnectionTester import ConnectionTest
from database import User


class log2action:
    def __init__(self):
        self.settingsFilePath = 'settings.json'
        self.cloudflareAPIURL = 'https://api.cloudflare.com/client/v4/'

    def getSettings(self):
        #   Read in the settings with user credentials
        settings = None
        with open(self.settingsFilePath) as f:
            settings = json.load(f)
        return settings

    def getFirewallLogs(self):
        settings = self.getSettings()
        if settings is not None:
            url = self.cloudflareAPIURL + 'zones/' + \
                settings['CF_ZONE_ID'] + '/security/events?limit=3'
            headers = {
                'X-Auth-Email': settings['CF_EMAIL_ADDRESS'],
                'X-Auth-Key': settings['CF_API_TOKEN'],
                'content-type': 'application/json'
            }
            request = requests.get(url, headers=headers).json()
            if request['success'] == True:
                print(request)
                print(request['result'][0]['source'])
        else:
            print(
                "\n\n\t[+]\t Could not communicate with Cloudflare API. Credentials provided are bad. Please fix credentials and try again.\n")
            print("\t[+]\t ERROR: \n")
            print("\t\t\t" + str(request))

    def run(self):
        if ConnectionTest().runTests():
            self.getFirewallLogs()
            print(str(User().__repr__))


if __name__ == '__main__':
    log2action().run()
