import json
import os
from util import Util

# Define the util object
util = Util()


class SettingsTester:
    def __init__(self):
        print(
            "\t[+]\t\t Testing provided config...")

    # Test to see if the file even exists
    def fileExists(self):
        retVal = False
        print(
            "\t[+]\t\t Looking for 'settings.json' file...")
        # See if 'settings.json' exists in the root direcotry.
        # wherver this file is... should be in /codebase
        if os.path.isfile(util.settingsFilePath):
            retVal = True
            print(
                "\t[+]\t\t Settings file found.")
        else:
            retVal = False
            print(
                "\t[!!]\t\t ERROR: Could not find a settings file names 'settings.json' in this directory! Please fix!")
        return retVal

    def checkValidJSON(self):
        retVal = False
        print(
            "\t[+]\t\t Validating the file format. Settings should be in the JSON format...")
        try:
            settings = util.getSettings()
            if settings is not None:
                print(
                    "\t[+]\t\t Settings file is in a valid JSON format.")
                retVal = True
        except:
            print(
                "\t[!!]\t\t ERROR: Incorrect file format. It needs to be JSON. Fix this issue and try again!")
            retVal = False
        return retVal

    def checkNeededKeys(self):
        print(
            "\t[+]\t\t Validating the settings has the required keys...")
        settings = util.getSettings()

        # Key definitions
        CF_API_TOKEN = "CF_API_TOKEN"
        CF_EMAIL_ADDRESS = "CF_EMAIL_ADDRESS"
        CF_ZONE_ID = "CF_ZONE_ID"
        LOG_REQUEST_DELAY = "LOG_REQUEST_DELAY"
        JS_CHALLENGE_LIMIT = "JS_CHALLENGE_LIMIT"
        CAPTCHA_CHALLENGE_LIMIT = "CAPTCHA_CHALLENGE_LIMIT"
        BAN_LIMIT = "BAN_LIMIT"
        NUM_JS_CHALLENGE_DAYS = "NUM_JS_CHALLENGE_DAYS"
        NUM_CAPTCHA_CHALLENGE_DAYS = "NUM_CAPTCHA_CHALLENGE_DAYS"
        NUM_BAN_WEEKS = "NUM_BAN_WEEKS"
        UNDO_ACTION_EVERY_XTH_HOUR = "UNDO_ACTION_EVERY_XTH_HOUR"

        #   --  Start seeing if the needed keys exist   --
        retVal = True

        # See if the Cloudflare API key exists.
        if settings[CF_API_TOKEN]:
            print(
                "\t[+]\t\t\t Success: Key: " + CF_API_TOKEN + " is OK!")
        else:
            retVal = False
            print(
                "\t[!!]\t\t\t ERROR: Key: " + CF_API_TOKEN + " does not exist. Please fix and try again!")

        # See if the Cloudflare email exists.
        if settings[CF_EMAIL_ADDRESS]:
            print(
                "\t[+]\t\t\t Success: Key: " + CF_EMAIL_ADDRESS + " is OK!")
        else:
            retVal = False
            print(
                "\t[!!]\t\t\t ERROR: Key: " + CF_EMAIL_ADDRESS + " does not exist. Please fix and try again!")

        # See if the Cloudflare zone ID exists.
        if settings[CF_ZONE_ID]:
            print(
                "\t[+]\t\t\t Success: Key: " + CF_ZONE_ID + " is OK!")
        else:
            retVal = False
            print(
                "\t[!!]\t\t\t ERROR: Key: " + CF_ZONE_ID + " does not exist. Please fix and try again!")
        # See if the time (in seconds) between delays has been set.
        if settings[LOG_REQUEST_DELAY]:
            print(
                "\t[+]\t\t\t Success: Key: " + LOG_REQUEST_DELAY + " is OK!")
        else:
            retVal = False
            print(
                "\t[!!]\t\t\t ERROR: Key: " + LOG_REQUEST_DELAY + " does not exist. Please fix and try again!")

        # See if the limit of requests to JS Challenge an IP exists.
        if settings[JS_CHALLENGE_LIMIT]:
            print(
                "\t[+]\t\t\t Success: Key: " + JS_CHALLENGE_LIMIT + " is OK!")
        else:
            retVal = False
            print(
                "\t[!!]\t\t\t ERROR: Key: " + JS_CHALLENGE_LIMIT + " does not exist. Please fix and try again!")

        # See if the limit of requests to CAPTCHA Challenge an IP exists.
        if settings[CAPTCHA_CHALLENGE_LIMIT]:
            print(
                "\t[+]\t\t\t Success: Key: " + CAPTCHA_CHALLENGE_LIMIT + " is OK!")
        else:
            retVal = False
            print(
                "\t[!!]\t\t\t ERROR: Key: " + CAPTCHA_CHALLENGE_LIMIT + " does not exist. Please fix and try again!")

        # See if the limit of requests to ban an IP exists.
        if settings[BAN_LIMIT]:
            print(
                "\t[+]\t\t\t Success: Key: " + BAN_LIMIT + " is OK!")
        else:
            retVal = False
            print(
                "\t[!!]\t\t\t ERROR: Key: " + BAN_LIMIT + " does not exist. Please fix and try again!")

        # See if the number of days a JS Challenge is in place for, exists.
        if settings[NUM_JS_CHALLENGE_DAYS]:
            print(
                "\t[+]\t\t\t Success: Key: " + NUM_JS_CHALLENGE_DAYS + " is OK!")
        else:
            retVal = False
            print("\t[!!]\t\t\t ERROR: Key: " + NUM_JS_CHALLENGE_DAYS +
                  " does not exist. Please fix and try again!")

        # See if the number of days a CAPTCHA Challenge is in place for, exists.
        if settings[NUM_CAPTCHA_CHALLENGE_DAYS]:
            print(
                "\t[+]\t\t\t Success: Key: " + NUM_CAPTCHA_CHALLENGE_DAYS + " is OK!")
        else:
            retVal = False
            print(
                "\t[!!]\t\t\t ERROR: Key: " + NUM_CAPTCHA_CHALLENGE_DAYS + " does not exist. Please fix and try again!")

        # See if the number of WEEKS a ban is in place for, exists.
        if settings[NUM_BAN_WEEKS]:
            print(
                "\t[+]\t\t\t Success: Key: " + NUM_BAN_WEEKS + " is OK!")
        else:
            retVal = False
            print("\t[!!]\t\t\t ERROR: Key: " + NUM_BAN_WEEKS +
                  " does not exist. Please fix and try again!")

        # See if the 'undoAction' every xth hour key, exists.
        if settings[UNDO_ACTION_EVERY_XTH_HOUR]:
            print(
                "\t[+]\t\t\t Success: Key: " + UNDO_ACTION_EVERY_XTH_HOUR + " is OK!")
        else:
            retVal = False
            print("\t[!!]\t\t\t ERROR: Key: " + UNDO_ACTION_EVERY_XTH_HOUR +
                  " does not exist. Please fix and try again!")

        ###                                ###
        #   ADD MORE TESTS IF NEEDED LATER   #
        ###                                ###

        if retVal:
            print(
                "\t[+]\t\t All keys in settings are valid!")
        # Return false if any test / keys is not found
        return retVal

    def runTests(self):
        retVal = False
        if self.fileExists() and self.checkValidJSON() and self.checkNeededKeys():
            retVal = True
        return retVal

# if __name__ == '__main__':
#     SettingsTester().checkNeededKeys()
