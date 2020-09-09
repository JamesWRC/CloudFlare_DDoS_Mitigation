#!/usr/bin/env python3

import json
import requests
import datetime
from datetime import timedelta
import time
from util import Util
import database
# Define th eutil object
util = Util()


class UndoAction:
    def __init__(self):
        pass

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

    def updateDatabase(self):
        # Get the JSON respose containing all Access Rules currently in place
        data = self.getAccessRules()
        try:
            for actionedHost in data["result"]:

                ipAddress = actionedHost['configuration']['value']
                uuid = actionedHost['id']
                notes = actionedHost['notes']
                actioned_date = actionedHost['created_on']
                # Get the time string but NOT the milliseconds?
                try:
                    # Add the try for safety, just incase Cloudflare changes their string format
                    actioned_date = actioned_date.split('.')[0]
                except:
                    pass
                # print(actioned_date)
                revoke_date = notes.split('REVOKE_DATE=')[1]

                database.ActionHistory().addActionHistory(
                    ipAddress, uuid, notes, actioned_date, revoke_date)
        except:
            print("An error occurred... response received:\n\n" + str(data))

    def undoActions(self):

        # Get the JSON respose containing all Access Rules currently in place
        data = database.ActionHistory().getRules()
        # print(data)
        currTime = datetime.datetime.now()
        try:
            for actionedHost in data:
                # Get the note
                revoke_date = actionedHost.revoke_date
                uiid = actionedHost.uiid

                proccessedDateTime = datetime.datetime.strptime(
                    revoke_date, '%Y-%m-%d %H:%M:%S')

                # If the current time is past the time to 'unaction' a host
                if currTime >= proccessedDateTime:

                    # Remove local record of action
                    self.removeRule(uiid)
        except:
            print("An error occurred... response received:\n\n" + str(data))

    def removeRule(self, uiid):
        # Send request off to Cloudflare, if successful then remove from local DB
        deleteRuleURL = util.getAccessRuleURL()
        deleteRuleURL += '/' + uiid

        # Send request
        response = requests.delete(
            deleteRuleURL, headers=util.getRequestHeaders())

        # If response is successful, then remove local record.
        if response.status_code and response.json()['success'] is True:
            database.ActionHistory().deleteRule(uiid)


# if __name__ == '__main__':
    # if ConnectionTest().runTests():
    # UndoAction().shouldPerformOnHour()
    # UndoAction().undoActions()
    # UndoAction().updateDatabase()
    # UndoAction().undoActions()
