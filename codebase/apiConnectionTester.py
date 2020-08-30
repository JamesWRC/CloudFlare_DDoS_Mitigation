#!/usr/bin/env python3

import json
import requests
import database
from util import Util

# define the util object
util = Util()


class ConnectionTest:
    def __init__(self):
        print("\t[+]\t\t Running API and network connection tests...")

        #   Test if the Docker container has an internet connection and can query for Cloudflare.

    def connectToCloudflare(self):
        print("\t[+]\t\t Trying to ping Cloudflare...")
        request = requests.get('https://www.cloudflare.com')
        if request.status_code == 200:
            #   Container successfully connected, return True.
            print("\t[+]\t\t Successfully pinged Cloudflare.")
            return True
        else:
            print("\t[!!]\t  ERROR: \n")
            print(
                "\t[!!]\t Container could not connect to the internet, or cannot resolve Cloudflare DNS.")
            return False

    def authenticationTest(self):
        print(
            "\t[+]\t\t Testing credentials user authentication...")
        # Get settings
        settings = util.getSettings()
        # Get the url needed for user details
        url = util.getUserDetailsURL()

        headers = {
            'X-Auth-Email': settings['CF_EMAIL_ADDRESS'],
            'X-Auth-Key': settings['CF_API_TOKEN'],
            'content-type': 'application/json'
        }

        # Make request to get user details
        response = requests.get(url, headers=headers)

        retVal = False
        if response.status_code == 200:
            retVal = True
            print(
                "\t[+]\t\t User credentials OK!")
        else:
            print(
                "\t[!!]\t\t ERROR: Bad ser credentials! \n")
            print("Response: " + str(response.json()))
        return retVal

    def graphQLTest(self):
        print(
            "\t[+]\t\t Attempting to communicate with Cloudflare API, and test credentials...")

        # Get settings
        settings = util.getSettings()

        retVal = None
        if settings is not None:
            # Create the request headers and specify the URL.
            url = util.getGraphQLURL()
            header = {
                'X-Auth-Email': settings['CF_EMAIL_ADDRESS'],
                'X-Auth-Key': settings['CF_API_TOKEN'],
                'content-type': 'application/json'
            }
            # Construct the GQL query to get logs.
            query = {"query": "query ListFirewallEvents($zoneTag: string, $filter: FirewallEventsAdaptiveFilter_InputObject) {\
                    viewer {\
                        zones(filter: {zoneTag: $zoneTag}) {\
                            firewallEventsAdaptive(\
                                filter: $filter\
                                limit: 1\
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
            # Make the request.
            request = requests.post(
                url, headers=header, json=query)
            #   Test if the success key in the JSON responce is there and is True
            if request.json()['errors'] == None:
                print(
                    "\t[+]\t\t Successfully communicated with Cloudflare API. Credentials provided are OK.")
                retVal = True
            else:
                print(
                    "\n\t[!!]\t\t Could not communicate with Cloudflare API. Credentials provided are bad. Please fix credentials and try again.\n")
                print("\t[!!]\t\t  ERROR: \n")
                print("\t\t\t\t" + str(request.json()))
                retVal = False

        return retVal

    def runTests(self):
        print(
        "\n\n\t[-]\t\t One moment, running a few network tests...\n\n")
        # Run tests
        if self.connectToCloudflare() and self.authenticationTest() and self.graphQLTest():
            return True
        else:
            print("\n\t[!!]\t   One or more preflight tests failed, meaning this tool may not work properly if at all. Fix these errors then try again.\n\n")
            raise ValueError(
                'One or more tests failed. View the log above, fix the error and try again! Terminating...')


# if __name__ == '__main__':
#     print(
#         "\n\n\t[+]    One moment, running a few tests before the tool starts.\n")
#     ConnectionTest().runTests()
