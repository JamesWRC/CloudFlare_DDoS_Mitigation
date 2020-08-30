#!/usr/bin/env python3

import json
import requests
import sqlalchemy
from apiConnectionTester import ConnectionTest
import database
import datetime
from datetime import timedelta
import time
from util import Util

# Define the util object
util = Util()
class log2action:
    def __init__(self):
        print("a")

    def getFirewallLogs(self):
        settings = util.getSettings()
        if settings is not None:
            url = util.getGraphQLURL()
            header = {
                'X-Auth-Email': settings['CF_EMAIL_ADDRESS'],
                'X-Auth-Key': settings['CF_API_TOKEN'],
                'content-type': 'application/json'
            }
            # Get current time in ISO format
            # UTC to ISO 8601 with TimeZone information (Python 3):
            currentISOTime = datetime.datetime.now(
            ).astimezone().replace(microsecond=0).isoformat()

            # Get last request time in ISO format.
            host = database.Visitors()
            lastVisitorRecorded = host.getLastHost()
            lastISOTime = lastVisitorRecorded
            # If there is no last request (db is empty)
            # then set to 24hrs ago in ISO format
            if lastISOTime is None:
                last_hour_date_time = datetime.datetime.now() - timedelta(hours=24)
                lastISOTime = last_hour_date_time.astimezone().replace(
                    microsecond=0).isoformat()
            else:
                lastISOTime = lastVisitorRecorded
                lastISOTime = lastISOTime.requested_at
            
            # Create the GQL query
            query = {"query": "query ListFirewallEvents($zoneTag: string, $filter: FirewallEventsAdaptiveFilter_InputObject) {\
                    viewer {\
                        zones(filter: {zoneTag: $zoneTag}) {\
                            firewallEventsAdaptive(\
                                filter: $filter\
                                limit: 1000\
                                orderBy: [datetime_ASC]\
                            ) {\
                                action\
                                clientAsn\
                                clientCountryName\
                                clientIP\
                                clientRequestPath\
                                clientRequestQuery\
                                datetime\
                                source\
                                userAgent\
                                rayName\
                            }\
                        }\
                    }\
                }",
                     "variables": {
                         "zoneTag": "d4ec936a3a25343c77ecb893fa6396a2",
                         "filter": {
                             "datetime_geq": str(lastISOTime),
                             "datetime_leq": str(currentISOTime)
                         }
                     }
                     }
            # Create request
            request = requests.post(
                url, headers=header, json=query)
            for obj in request.json()["data"]["viewer"]["zones"][0]["firewallEventsAdaptive"]:
                # Only enter a record if there is no previous record in the database
                # OR if the last record in the databases ray_name DOES NOT equal the last rayName from the API call
                if lastVisitorRecorded is None or lastVisitorRecorded.ray_name != obj["rayName"]:
                    # Add visitor to the database
                    host.addVisitor(action=obj["action"], ip_address=obj["clientIP"], user_agent=obj["userAgent"], path=obj["clientRequestPath"], query_string=obj["clientRequestQuery"],
                                    asn=obj["clientAsn"], country=obj["clientCountryName"], rule_id=obj["source"], requested_at=obj["datetime"], ray_name=obj["rayName"])
        else:
            print(
                "\n\n\t[+]\t Could not communicate with Cloudflare API. Credentials provided are bad. Please fix credentials and try again.\n")
            print("\t[+]\t ERROR: \n")
            print("\t\t\t" + str(request))


    def action(self):
        # Here we will query the database to get the IP addresses and take action
        # based on the number of times an IP addrss has made requests in 1 minute

        records = database.Visitors().getUniqueIPs()
        for hostIP in records:
            # Get number of request the IP address has made
            requestCount = database.Visitors().getNumberOfRequestsFromIP(hostIP)
            settings = util.getSettings()
            # If request is less then pre defined settings
            # DEFAULT SETTINGS:
            #   JS_CHALLENGE_LIMIT = 90
            #       --> 1.5 requests per second, perfectly fine, just heavy use.

            #   CAPTCHA_CHALLENGE_LIMIT = 120
            #       --> 2 requests per second, could be ok, but should be discouraged,
            #           thus will be shown a CAPTCHA Challenge.

            #   BAN_LIMIT = 300 --> thats 5 requests per second in 1 min.
            #       --> 5 requests per second. This is unacceptable for most standard
            #           sites. Thus will be banned. This IP is malicious.
            timeOfIncident = datetime.datetime.now()

            # Create the vars that hold the amount of time that 
            # an action should be applied for
            appliedTillDay = timeOfIncident + \
                timedelta(days=settings["NUM_JS_CHALLENGE_DAYS"])
            appliedTillWeek = timeOfIncident + \
                timedelta(days=settings["NUM_CAPTCHA_CHALLENGE_DAYS"])
            appliedTillMonth = timeOfIncident + \
                timedelta(weeks=settings["NUM_BAN_WEEKS"])  # ~ 3 months (default settings)

            # set the IPaddress type ( IPv4 or IPv6 )
            IPAddressType = "ip"
            # Default IPv4 addres is 15 chars long 
            if len(hostIP) > 15:
                IPAddressType = "ip6"

            # Perform a JS (JavaScript) Challenge
            if requestCount >= settings["JS_CHALLENGE_LIMIT"] \
                    and requestCount < settings["CAPTCHA_CHALLENGE_LIMIT"]:
                print("Javascript challenging")
                self.makeAPIcall(IPAddressType, hostIP, "js_challenge", "IP made ~" + str(requestCount) +
                                 " requests detected @ " + str(timeOfIncident.strftime("%Y-%m-%d %H:%M:%S")) + ", REVOKE_DATE=" + str(appliedTillDay.strftime("%Y-%m-%d %H:%M:%S")))

            # Perform a CAPTCHA Challenge.
            elif requestCount >= settings["CAPTCHA_CHALLENGE_LIMIT"] \
                    and requestCount < settings["BAN_LIMIT"]:
                print("CAPTCHA challenging")
                self.makeAPIcall(
                    IPAddressType, hostIP, "challenge", "IP made >= " + str(requestCount) + ", detected @ " + str(timeOfIncident) + " REVOKE_DATE=" + str(appliedTillWeek))

            # Perform a ban.
            elif requestCount >= settings["BAN_LIMIT"]:
                print("BAN")
                self.makeAPIcall(IPAddressType, hostIP, "block", "IP made >= " + str(requestCount) +
                                 ", detected @ " + str(timeOfIncident) + " REVOKE_DATE=" + str(appliedTillMonth))

    def run(self):
        # Run for 1 minute
        currentTime = datetime.datetime.now()
        endTime = currentTime + timedelta(minutes=0.1)

        settings = util.getSettings()
        # Define how long to wait before making another request
        sleepTime = settings["LOG_REQUEST_DELAY"]

        while currentTime <= endTime:
            print(currentTime)
            print(endTime)
            # Log firewall to database
            self.getFirewallLogs()

            # Update while loop params
            currentTime = datetime.datetime.now()
            time.sleep(sleepTime)

        # Take actions on the past minute of logs
        self.action()

        # Remove all rows in the Visitors table.
        database.Visitors().deleteAllRows()

    def makeAPIcall(self, addressType, IPaddress, action, reason):
        settings = util.getSettings()
        # Get the access rule URL
        url = util.getAccessRuleURL()

        header = {
            'X-Auth-Email': settings['CF_EMAIL_ADDRESS'],
            'X-Auth-Key': settings['CF_API_TOKEN'],
            'content-type': 'application/json'
        }
        # Create the data based of the host request count, IP and reason note
        data = '{\
            "mode":' + "\"" + action + "\"" + ',\
            "configuration":{\
                "target":' + "\"" + addressType + "\"" + ',\
                "value":' + "\"" + IPaddress + "\"" + '\
                    },\
                "notes":' + "\"" + reason + "\"" + '\
                }'
        # Create the request
        request = requests.post(
            url, headers=header, data=data)


if __name__ == '__main__':
    # if ConnectionTest().runTests():
    log2action().run()
    log2action().run()
