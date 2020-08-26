from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
db_engine = create_engine('sqlite:///database.sqlite3')
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
                         Column('method', String(10)),
                         Column('path', String(256)),
                         Column('query_string', String(256)),
                         Column('asn', String(256)),
                         Column('country', String(256)),
                         Column('rule_id', String(256)),
                         Column('requested_at', String(256)),
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
        print("\n\t[+]\t Building Database...")
        Base.metadata.create_all(db_engine)


##############  Below are the classes of the database. ##############

class Visitors(Base):
    #   The visitors of the site / resource
    __tablename__ = 'visitors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip_address = Column(String)
    user_agent = Column(String)
    method = Column(String)
    path = Column(String)
    query_string = Column(String)
    asn = Column(String)
    country = Column(String)
    rule_id = Column(String)
    requested_at = Column(String)

    # def __init__(self, ip_address, user_agent, method, path, query_string,
    #              asn, country, rule_id):
    #     self.ip = ip_address
    #     self.user_agent = user_agent
    #     self.method = method
    #     self.path = path
    #     self.query_string = query_string
    #     self.asn = asn
    #     self.country = country
    #     self.rule_id = rule_id

    def addVisitor(self, ip_address, user_agent, method, path, query_string,
                   asn, country, rule_id, requested_at):
        #   Create a new visitor to the database.
        visitor = Visitors()
        visitor.ip_address = ip_address
        visitor.user_agent = user_agent
        visitor.method = method
        visitor.path = path
        visitor.query_string = query_string
        visitor.asn = asn
        visitor.country = country
        visitor.rule_id = rule_id
        visitor.requested_at = requested_at
        session.add(visitor)
        session.commit()

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


if __name__ == '__main__':

    #   build tables
    print("hello")
    Database().buildDatabaseTables()

    #   Test data
    # Visitors().addVisitor('127.0.0.1', 'iOS', 'GET', '/', 'index', 'AU', 'Melb', '123')
    # LogHistory().addLogHistory('a', 'b')
