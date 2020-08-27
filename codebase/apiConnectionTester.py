#!/usr/bin/env python3

import json
import requests
import database


class ConnectionTest:
    def __init__(self):
        self.settingsFilePath = 'settings.json'
        self.cloudflareAPIURL = 'https://api.cloudflare.com/client/v4/'
        print(
            "\n\n\t[+]    One moment, running a few tests before the tool starts.\n")

    def testConnectionToCloudFlareAPI(self):
        print(
            "\t[+]\t\t Attempting to communicate with Cloudflare API, and test credentials...")

        #   Read in the settings with user credentials
        settings = None
        with open(self.settingsFilePath) as f:
            settings = json.load(f)
        #   Ensure that there is actual data in this variable. IE the file successfully opened
        if settings is not None:
            #   Create the request headers and specify the URL
            url = self.cloudflareAPIURL + 'zones/' + \
                settings['CF_ZONE_ID'] + '/security/events?limit=1'
            headers = {
                'X-Auth-Email': settings['CF_EMAIL_ADDRESS'],
                'X-Auth-Key': settings['CF_API_TOKEN'],
                'content-type': 'application/json'
            }
            #   Make the request
            request = requests.get(url, headers=headers).json()
            #   Test if the success key in the JSON responce is there and is True
            if request['success'] == True:
                print(
                    "\t[+]\t\t Successfully communicated with Cloudflare API. Credentials provided are OK.")
                return True
            else:
                print(
                    "\n\t[+]\t\t Could not communicate with Cloudflare API. Credentials provided are bad. Please fix credentials and try again.\n")
                print("\t[+]\t\t  ERROR: \n")
                print("\t\t\t\t" + str(request))

    #   Test if the Docker container has an internet connection and can query for Cloudflare.
    def connectToCloudflare(self):
        print("\t[+]\t\t Trying to ping Cloudflare...")
        request = requests.get('https://www.cloudflare.com')
        if request.status_code == 200:
            #   Container successfully connected, return True.
            print("\t[+]\t\t Successfully pinged Cloudflare.")
            return True
        else:
            print("\t[+]\t  ERROR: \n")
            print(
                "\t[+]\t Container could not connect to the internet, or cannot resolve Cloudflare DNS.")
            return False

    def graphQL(self):
        print(
            "\t[+]\t\t Attempting to communicate with Cloudflare API, and test credentials...")

        #   Read in the settings with user credentials
        settings = None
        with open(self.settingsFilePath) as f:
            settings = json.load(f)
        #   Ensure that there is actual data in this variable. IE the file successfully opened
        if settings is not None:
            #   Create the request headers and specify the URL
            # url = self.cloudflareAPIURL + 'zones/' + \
            #     settings['CF_ZONE_ID'] + '/security/events?limit=1000'
            url = "https://api.cloudflare.com/client/v4/graphql/"
            header = {
                'X-Auth-Email': settings['CF_EMAIL_ADDRESS'],
                'X-Auth-Key': settings['CF_API_TOKEN'],
                'content-type': 'application/json'
            }

            query = {"query": "query ListFirewallEvents($zoneTag: string, $filter: FirewallEventsAdaptiveFilter_InputObject) {\
                    viewer {\
                        zones(filter: {zoneTag: $zoneTag}) {\
                            firewallEventsAdaptive(\
                                filter: $filter\
                                limit: 1000\
                                orderBy: [datetime_DESC]\
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
                            }\
                        }\
                    }\
                }",
                     "variables": {
                         "zoneTag": "d4ec936a3a25343c77ecb893fa6396a2",
                         "filter": {
                             "datetime_geq": "2020-08-26T02:59:49.023731728Z",
                             "datetime_leq": "2020-08-27T02:59:49.023731728Z"
                         }
                     }
                     }
            request = requests.post(
                url, headers=header, json=query)
            # print(request.json())
            for a in request.json()["data"]["viewer"]["zones"][0]["firewallEventsAdaptive"]:
                print(a)
                print("---")
                print(a["clientIP"])
                host = database.Visitors()
                host.addVisitor(action=a["action"], ip_address=a["clientIP"], user_agent=a["userAgent"], path=a["clientRequestPath"], query_string=a["clientRequestQuery"],
                                asn=a["clientAsn"], country=a["clientCountryName"], rule_id=a["source"], requested_at=a["datetime"])
                print("---")

            # result = schema.execute(qu, variable_values={"zoneTag": "12321",
            #                                              "filter": {
            #                                                  "datetime_geq": "2020-07-26T01:00:00Z",
            #                                                  "datetime_leq": "2020-07-27T23:00:00Z"
            #                                              }})

            # gql_variables = {
            #     "zoneTag": settings['CF_ZONE_ID'],
            #     "filter": {
            #         "datetime_geq": "2020-07-26T01:00:00Z",
            #         "datetime_leq": "2020-07-27T23:00:00Z"
            #     }
            # }
            # query = {
            #     "query": str(gql_query.replace("\n", "").replace(" ", "")),
            #     "variables": str(gql_variables)
            # }
            # print(result['data'])
            exit(0)
            #   Make the request
            # request = requests.post(
            #     url, data=a, headers=headers).json()
            # print(request)
            # #   Test if the success key in the JSON responce is there and is True
            # if request['success'] == True:
            #     print(
            #         "\t[+]\t\t Successfully communicated with Cloudflare API. Credentials provided are OK.")
            #     return True
            # else:
            #     print(
            #         "\n\t[+]\t\t Could not communicate with Cloudflare API. Credentials provided are bad. Please fix credentials and try again.\n")
            #     print("\t[+]\t\t  ERROR: \n")
            #     print("\t\t\t\t" + str(request))

            #   The 'MAIN' method to run the tests.

    def runTests(self):
        print("\t[+]\t\t Running preflight tests...")
        testResults = self.connectToCloudflare()
        if testResults:
            testResults = self.testConnectionToCloudFlareAPI()
        if testResults:
            print("\t[+]\t\t   All preflight tests have passed successfully...")

            print("\t[+]\t\t Launching services, now...\n\n")
        else:
            print("\n\t[+]\t   One or more preflight tests failed, meaning this tool may not work properly if at all. Fix these errors then try again.\n\n")
        return testResults


if __name__ == '__main__':
    ConnectionTest().runTests()
    print("\n\n\n == == == ==\n\n\n")
    ConnectionTest().graphQL()
