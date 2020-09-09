import json
import requests


class Util:
    def __init__(self):
        self.rootWorkingDirectory = 'codebase/'
        self.settingsFilePath = self.rootWorkingDirectory + 'settings.json'
        self.cloudflareAPIURL = 'https://api.cloudflare.com/client/v4/'
        self.databaseFileName = 'database.sqlite3'

    # Open the settings.json file and return the object
    def getSettings(self):
        settings = None
        with open(self.settingsFilePath) as f:
            settings = json.load(f)
        return settings

    # Returns URL for user details
    def getUserDetailsURL(self):
        return self.cloudflareAPIURL + 'user/'

    # Returns the GraphQL URL
    def getGraphQLURL(self):
        return self.cloudflareAPIURL + 'graphql/'

    # Make request to take an action on a host.
    def getAccessRuleURL(self):
        return self.cloudflareAPIURL + 'zones/' + \
            self.getSettings()['CF_ZONE_ID'] + '/firewall/access_rules/rules'

    def getRequestHeaders(self):
        settings = self.getSettings()
        return {
            'X-Auth-Email': settings['CF_EMAIL_ADDRESS'],
            'X-Auth-Key': settings['CF_API_TOKEN'],
            'content-type': 'application/json'
        }

    def printLabel(self):
        title = """
         _____ _                 _  __ _
        / ____| |               | |/ _| |
       | |    | | ___  _   _  __| | |_| | __ _ _ __ ___
       | |    | |/ _ \| | | |/ _` |  _| |/ _` | '__/ _ \\
       | |____| | (_) | |_| | (_| | | | | (_| | | |  __/
        \_____|_|\___/ \__,_|\__,_|_| |_|\__,_|_|  \___|
         _____       _         _ _           _ _
        |  __ \     | |       | (_)         (_) |
        | |__) |__ _| |_ ___  | |_ _ __ ___  _| |_ ___ _ __
        |  _  // _` | __/ _ \ | | | '_ ` _ \| | __/ _ \ '__|
        | | \ \ (_| | ||  __/ | | | | | | | | | ||  __/ |
        |_|  \_\__,_|\__\___| |_|_|_| |_| |_|_|\__\___|_|
        \n\t ~ Witten and maintained by github.com/JamesWRC ~

        +\tStop DDoS attacks more quickly.
        +\tRate limit users.
        +\tSave server resources.
        +\tReduce serverless costs.

        Disclaimer:
        All API and data is provided by the kindness of Cloudflare.
        This is a free alternative to a ratelimiter using the Cloudflare API.
        This will only work if your site is being proxied by Cloudflare.
        If you need a more reliable rate limiter and services to stop
        DDoS attacks, then upgrade your Cloudflare account and purchase the
        Cloudflare Rate Limiter services.
        \n
        This tool is free, open source and provided AS IS. There are no guarantees
        that this tool will help protect or save you money in anyway. Do not abuse
        Cloudflares API. Use this tool at your own risk.
        """
        print(title)


if __name__ == '__main__':
    Util().getAllAccessRules()
