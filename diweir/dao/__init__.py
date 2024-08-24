from datetime import datetime
from diweir.utils.connections import MetadataConnection
from sqlalchemy import select, insert
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine.interfaces import DBAPICursor

# Commented out as will be required later. Currently only SQLAlchemy is accomodateded.
# meta = MetaData(schema="DIWEIR")
# Base = declarative_base(metadata=meta)

Base = declarative_base()

# Commented out for reference
# class PiiType(Base):
#     __tablename__ = "PII_TYP"
#     typ = Column("TYP", String, primary_key = True)
#     desc = Column("DSCRB", String)
#
# class DBProvider(Base):
#     __tablename__ = "DB_PRVDR"
#     provider = Column("PRVDR", String, primary_key=True)
#     name = Column("NAME", String, unique=True)
#
# class Environment(Base):
#     __tablename__ = "ENV"
#     name = Column("NAME", String, primary_key = True)
#     desc = Column("DSCRB", String)
#
# class Databases(Base):
#     __tablename__ = "DB"
#     name = Column("NAME", String, primary_key = True)
#     env = Column("ENV", String, ForeignKey("ENV.NAME"))
#     provider = Column("PVDR", String, ForeignKey("DB_PRVDR.PRVDR"))
#     username = Column("USER", String, nullable=False)
#     password = Column("PWD", String, nullable=False)
#     host = Column("HOST", String, nullable=False)
#     port = Column("PORT", Integer, nullable=False)
#     schema = Column("SCHEMA", String, nullable=False)
#
# class ArchivalDetails(Base):
#     __tablename__ = "ARCHV_DTLS"
#     id = Column("ID", Integer, primary_key=True)
#     enabled = Column("ENABLE", Boolean, nullable=False)
#     db = Column("DB", String, ForeignKey('DB.NAME'))
#     schema = Column("SCHEMA", String, nullable=False)
#     table = Column("TABLE", String, nullable=False)
#     date_column = Column("DT_CLMN", String, nullable=True) # If this is not provided the referential column needs to be provided
#     date_from = Column("FROM", DateTime, nullable=True)
#     date_to = Column("TO", DateTime, nullable=True)
#     reference_table = Column("RFRNC_TBL", String, nullable=True) # Needs to be a table with a relation(parent/child) to the table
#     reference_column = Column("RFRNC_COL", String, nullable=True)
#
# class PurgeDetails(Base):
#     __tablename__ = "PRG_DTLS"
#     id = Column("ID", Integer, primary_key=True)
#     enabled = Column("ENABLE", Boolean, nullable=False)
#     db = Column("DB", String, ForeignKey('DB.NAME'))
#     schema = Column("SCHEMA", String, nullable=False)
#     table = Column("TABLE", String, nullable=False)
#     date_column = Column("DT_CLMN", String, nullable=True) # If this is not provided the referential column needs to be provided
#     date_from = Column("FROM", DateTime, nullable=True)
#     date_to = Column("TO", DateTime, nullable=True)
#     reference_table = Column("RFRNC_TBL", String, nullable=True) # Needs to be a table with a relation(parent/child) to the table
#     reference_column = Column("RFRNC_COL", String, nullable=True)
#
# class MigrationDetails(Base):
#     __tablename__ = "MGRT_DTLS"
#     id = Column("ID", Integer, primary_key=True)
#     enabled = Column("ENABLE", Boolean, nullable=False)
#     db = Column("DB", String, ForeignKey('DB.NAME'))
#     schema = Column("SCHEMA", String, nullable=False)
#
# class AnonymizationDetails(Base):
#     __tablename__ = "ANON_DTLS"
#     id = Column("ID", Integer, primary_key=True)
#     enabled = Column("ENABLE", Boolean, nullable=False)
#     db = Column("DB", String, ForeignKey('DB.NAME'))
#     schema = Column("SCHEMA", String, nullable=False)
#     table = Column("TABLE", String, nullable=False)
#     column = Column("COL", String, nullable=False)
#     len = Column("LEN", Integer, nullable=True)
#     pii_typ = Column("PII_TYP", String, ForeignKey("PII_TYP.TYP"))
#
# class Processes(Base):
#     __tablename__ = "PROC_LIST"
#     name = Column("NAME", String, primary_key = True)
#     desc = Column("DESC", String)
#
# class DatabaseProcessStatus(Base):
#     __tablename__ = "PROC_DB"
#     id = Column("ID", Integer, primary_key=True)
#     typ = Column(String)
#     db = Column("DB", String)
#     start_time = Column("START", DateTime, nullable=False)
#     end_time = Column("END", DateTime)
#     status = Column("STATUS", String, nullable=False)
#
# class TableProcessStatus(Base):
#     __tablename__ = "PROC_TBL"
#     id = Column("ID", Integer, primary_key=True)
#     proc_db = Column(Integer, ForeignKey("PROC_DB.ID"))
#     table = Column("TABLE", String, nullable=False)
#     start_time = Column("START", DateTime, nullable=False)
#     end_time = Column("END", DateTime)
#     status = Column("STATUS", String, nullable=False)


def initialize(conn: MetadataConnection):
    # Common tables - Data definition
    from .common import DBProvider, Environment, User, Roles
    from diweir.config.master_data import db_providers, envs

    db_stmt = insert(DBProvider).values(db_providers)
    pre_env_stmt = {
        "created_on": datetime.now(),
        "modified_on": datetime.now(),
        "created_by": "admin",
        "modified_by": "admin",
    }
    env_stmt = insert(Environment).values([{**env, **pre_env_stmt} for env in envs])

    # Initialize the below
    # user_stmt = insert(User).values([])
    # roles_stmt = insert(Roles).values([])
    try:
        with conn.engine.connect() as cursor:
            cursor.execute(db_stmt)
            cursor.execute(env_stmt)
            cursor.commit()
            # Implement when initialized
            # cursor.execute(user_stmt)
            # cursor.execute(roles_stmt)
    except IntegrityError: 
        pass

    # Anonymization tables - Data definition
    from .anonymization import PiiType
    from diweir.config.master_data import anonymization_map

    # cursor.execute()
