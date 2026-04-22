from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url = "postgresql://postgres:root1234@localhost:5432/telusko"
engine = create_engine(db_url)
Session = sessionmaker(autocommit = False, autoflash = False, bind = engine)
#sessionmaker 
#   -->A configuration tool (factory) that creates a Session class.
#   -->You don't want to manually configure your connection settings every time you need to talk to the DB.

#autocommit = False
#   -->Prevents the session from automatically "saving" every change immediately.
#   -->This allows you to group multiple changes into a single Transaction. If one part fails, you can roll back everything.

#autoflush = False
#   -->Stops the session from sending changes to the database before every query.
#   -->When True, SQLAlchemy "flushes" (sends pending changes) to the DB every time you run a SELECT. Setting it to False gives you more manual control over performance.

#bind = engine
#   -->Connects this session factory to a specific database engine.
#   -->It tells the session which database it is actually talking to.