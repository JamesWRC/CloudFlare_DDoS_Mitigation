#!/usr/bin/env python3

import json
import requests
import sqlalchemy
from apiConnectionTester import ConnectionTest
import database
import datetime
from datetime import timedelta


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
            url = "https://api.cloudflare.com/client/v4/graphql/"
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

            request = requests.post(
                url, headers=header, json=query)
            for obj in request.json()["data"]["viewer"]["zones"][0]["firewallEventsAdaptive"]:
                # Only enter a record if there is no previous record in the database
                # OR if the last record in the databases ray_name DOES NOT equal the last rayName from the API call
                if lastVisitorRecorded is None or lastVisitorRecorded.ray_name != obj["rayName"]:
                    print("-----")
                    print(obj)
                    print("-----")
                    host.addVisitor(action=obj["action"], ip_address=obj["clientIP"], user_agent=obj["userAgent"], path=obj["clientRequestPath"], query_string=obj["clientRequestQuery"],
                                    asn=obj["clientAsn"], country=obj["clientCountryName"], rule_id=obj["source"], requested_at=obj["datetime"], ray_name=obj["rayName"])
        else:
            print(
                "\n\n\t[+]\t Could not communicate with Cloudflare API. Credentials provided are bad. Please fix credentials and try again.\n")
            print("\t[+]\t ERROR: \n")
            print("\t\t\t" + str(request))

            # Notes
            # need to figure out how to rapidly call requests one min ago (from current call)
            # query whole database and count number of requests by IP over a minutes
            # after 1 minute drop all rows of Visitors.

    def run(self):
        if ConnectionTest().runTests():
            self.getFirewallLogs()
            a = database.Visitors().getUniqueIPs()
            for b in a:
                print(b)
                print(database.Visitors().getNumberOfRequestsFromIP(b))

            # print(str(User().__repr__))


if __name__ == '__main__':
    log2action().run()
