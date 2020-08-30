from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from util import Util
import os
# Define the util object
util = Util()

Base = declarative_base()
db_engine = create_engine('sqlite:///' + util.databaseFileName)
# Try changing this to True and see what happens
db_engine.echo = False
metadata = MetaData(db_engine)

Session = sessionmaker(bind=db_engine)
Session.configure(bind=db_engine)
session = Session()


class Database:
    def createVisitors(self):
        #   Visitors table holds
        visitors = Table('visitors', metadata,
                         Column('ip_Address', String(40)),
                         Column('user_agent', String(256)),
                         Column('path', String(256)),
                         Column('query_string', String(256)),
                         Column('asn', String(256)),
                         Column('country', String(256)),
                         Column('rule_id', String(256)),
                         Column('requested_at', String(256)),
                         Column('ray_name', String(32)),
                         )
        visitors.create()

    def createLogHistory(self):
        logHistory = Table('logHistory', metadata,
                           Column('before_cursor', String(40)),
                           Column('after_cursor', String(256)),
                           )
        logHistory.create()

    def run(self):
        self.createVisitors()
        self.createLogHistory()

    def buildDatabaseTables(self):
        print("\n\t[+]\t\t Building Database...")
        Base.metadata.create_all(db_engine)

    def testDatabaseExists(self):
        print(
                "\n\n\t[-]\t\t Testing the database...\n\n")
        # Test to see if database exists
        if os.path.isfile(util.databaseFileName):
            retVal = True
            print(
                "\t[+]\t\t Database exists, OK.")
        else:
            retVal = False
            print(
                "\t[+]\t\t ERROR: Database not found! This is ok if you are running the tool in a Docker container\
                \n\t\t\t\tand the container is starting up...")
            print("\t[+]\t\t INFO: Building a clean database...\n\n")

            # Build database 
            Database().buildDatabaseTables()
        return retVal


##############  Below are the classes of the database. ##############

class Visitors(Base):
    #   The visitors of the site / resource
    __tablename__ = 'visitors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip_address = Column(String)
    action = Column(String)
    user_agent = Column(String)
    path = Column(String)
    query_string = Column(String)
    asn = Column(String)
    country = Column(String)
    rule_id = Column(String)
    requested_at = Column(String)
    ray_name = Column(String)

    def addVisitor(self, action, ip_address, user_agent, path, query_string,
                   asn, country, rule_id, requested_at, ray_name):
        #   Create a new visitor to the database.
        visitor = Visitors()
        visitor.ip_address = ip_address
        visitor.action = action
        visitor.user_agent = user_agent
        visitor.path = path
        visitor.query_string = query_string
        visitor.asn = asn
        visitor.country = country
        visitor.rule_id = rule_id
        visitor.requested_at = requested_at
        visitor.ray_name = ray_name
        session.add(visitor)
        session.commit()

    def getUniqueIPs(self):
        # Returns a list of unique IP addresses in the Database.
        query = session.query(
            Visitors.ip_address.distinct().label("ip_address"))
        titles = [row.ip_address for row in query.all()]
        return titles

    def getNumberOfRequestsFromIP(self, ip):
        count = session.query(Visitors).filter(
            Visitors.ip_address == ip).count()
        return count

    def getLastHost(self):
        lastHost = session.query(Visitors).order_by(Visitors.id.desc()).first()
        return lastHost

    def deleteAllRows(self):
        session.query(Visitors).delete()
        session.commit()
        print("delete all")

    def __repr__(self):
        #   Return the record in a string format
        return "< Visitor(IP Address='%s', user_agent='%s', method='%s', path='%s', \
                          query_string='%s', asn='%s', country='%s', rule_id='%s') >" % (self.ip_address, self.user_agent, self.method,
                                                                                         self.path, self.query_string, self.asn, self.country, self.rule_id)


class LogHistory(Base):
    #   This will store the request log cursors.
    #   Will keep a record of where we are up to in the Cloudflare logs.
    __tablename__ = 'logHistory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    before_cursor = Column(String)
    after_cursor = Column(String)

    def addLogHistory(self, before, after):
        log = LogHistory(before_cursor=before, after_cursor=after)
        session.add(log)
        session.commit()

    def __repr__(self):
        return "< LogHostory(before_cursor='%s', after_cursor='%s')> " & (self.before_cursor, self.after_cursor)


# if __name__ == '__main__':
#     #   build tables
#     Database().buildDatabaseTables()
