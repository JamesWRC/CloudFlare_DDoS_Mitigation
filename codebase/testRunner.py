from settingsTester import SettingsTester
from apiConnectionTester import ConnectionTest
from database import Database
from util import Util
import time

# Create the util object
util = Util()
# This class runs all tests, it will be a good indicator if anything is wrong.
class TestRunner:
    def __init__(self):
        # Show the banner and disclaimer
        util.printLabel()
        print("\n\n\n\t[-]\t Waiting 1 minute...")
        time.sleep(50)
        print(
                "\n\n\n\t[-]\t Running some tests before we start. This may take a while...\n\n")
        time.sleep(10)
            

    def run(self):
        retVal = False
        # Run tests on settings and the connection
        if SettingsTester().runTests() and ConnectionTest().runTests():

            # Run tests on the database
            dbRetVal = Database().testDatabaseExists()

            print("\n\n\t[+]\t All preflight tests have passed successfully...")

            print("\t[+]\t Launching services, now...\n\n")
            retVal = True
        if not retVal:
            print(
                "\n\n\n\t[!!!]\tERROR:\n\n\t\tOne or more tests failed! You need to fix these errors. View the above log to see what failed and\
                \n\t\tfix them. This tool will fail to run if the tests fail. If you are having isses find help here: \
                \n\t\thttps://github.com/JamesWRC/CloudFlare_DDoS_Mitigation/issues  \n\n")
            # Return a fail code.
            return 0
        # Return a success code.
        return 1

if __name__ == '__main__':
    TestRunner().run()