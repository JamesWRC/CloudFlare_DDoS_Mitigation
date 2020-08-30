#!/usr/bin/env python3

import json
import requests
import datetime
from datetime import timedelta
import time
from util import Util

# Define th eutil object
util = Util()
class UndoAction:
    def __init__(self):
        print("a")

    def shouldPerformOnHour(self):
        # Get settings
        settings = util.getSettings()

        # Define current time
        currTime = datetime.datetime.now()
        currHour = currTime.hour
        retVal = False
        if currHour % settings["UNDO_ACTION_EVERY_XTH_HOUR"] == 0:
            retVal = True
        return retVal

    def getAccessRules(self):
        settings = util.getSettings()
        if settings:

            # Get the access rules URL 
            url = util.getAccessRuleURL()
            headers = {
                'X-Auth-Email': settings['CF_EMAIL_ADDRESS'],
                'X-Auth-Key': settings['CF_API_TOKEN'],
                'content-type': 'application/json'
            }

            # Define the API calls params
            params = (
                ('page', '1'),
                ('per_page', '1000'),
            )

            # Make the request
            response = requests.get(url, headers=headers, params=params)
            
            # Return the JSON response
            return response.json()

    def undoActions(self):

        # Get the JSON respose containing all Access Rules currently in place
        data = self.getAccessRules()

        currTime = datetime.datetime.now()
        try:
            for actionedHost in data["result"]:
                # Get the note
                note = actionedHost["notes"]

                # Get the 'unaction' time specified in the note
                dateTillActionIsUndone = note.split("REVOKE_DATE=")[1]
                proccessedDateTime = datetime.datetime.strptime(
                    dateTillActionIsUndone, '%Y-%m-%d %H:%M:%S')
                # If the current time is past the time to 'unaction' a host
                if currTime >= proccessedDateTime:
                    print("can 'unaction' now")
        except:
            print("An error occurred... response received:\n\n" + str(data))


if __name__ == '__main__':
    # if ConnectionTest().runTests():
    UndoAction().shouldPerformOnHour()
    UndoAction().undoActions()
