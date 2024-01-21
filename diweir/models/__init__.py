from sqlalchemy import Boolean, Column, DateTime, Engine, ForeignKey, Integer, MetaData, String, insert
from sqlalchemy.orm import declarative_base

# meta = MetaData(schema="DIWEIR")
# Base = declarative_base(metadata=meta)
Base = declarative_base()

class PiiType(Base):
    __tablename__ = "PII_TYP"
    typ = Column("TYP", String, primary_key = True)
    desc = Column("DSCRB", String)

class DBProvider(Base):
    __tablename__ = "DB_PRVDR"
    provider = Column("PRVDR", String, primary_key=True)
    name = Column("NAME", String, unique=True)

class Environment(Base):
    __tablename__ = "ENV"
    name = Column("NAME", String, primary_key = True)
    desc = Column("DSCRB", String)

class Databases(Base):
    __tablename__ = "DB"
    name = Column("NAME", String, primary_key = True)
    env = Column("ENV", String, ForeignKey("ENV.NAME"))
    provider = Column("PVDR", String, ForeignKey("DB_PRVDR.PRVDR"))
    username = Column("USER", String, nullable=False)
    password = Column("PWD", String, nullable=False)
    host = Column("HOST", String, nullable=False)
    port = Column("PORT", Integer, nullable=False)
    schema = Column("SCHEMA", String, nullable=False)

class ArchivalDetails(Base):
    __tablename__ = "ARCHV_DTLS"
    id = Column("ID", Integer, primary_key=True)
    enabled = Column("ENABLE", Boolean, nullable=False)
    db = Column("DB", String, ForeignKey('DB.NAME'))
    schema = Column("SCHEMA", String, nullable=False)
    table = Column("TABLE", String, nullable=False)
    date_column = Column("DT_CLMN", String, nullable=True) # If this is not provided the referential column needs to be provided
    date_from = Column("FROM", DateTime, nullable=True)
    date_to = Column("TO", DateTime, nullable=True)
    reference_table = Column("RFRNC_TBL", String, nullable=True) # Needs to be a table with a relation(parent/child) to the table
    reference_column = Column("RFRNC_COL", String, nullable=True)

class PurgeDetails(Base):
    __tablename__ = "PRG_DTLS"
    id = Column("ID", Integer, primary_key=True)
    enabled = Column("ENABLE", Boolean, nullable=False)
    db = Column("DB", String, ForeignKey('DB.NAME'))
    schema = Column("SCHEMA", String, nullable=False)
    table = Column("TABLE", String, nullable=False)
    date_column = Column("DT_CLMN", String, nullable=True) # If this is not provided the referential column needs to be provided
    date_from = Column("FROM", DateTime, nullable=True)
    date_to = Column("TO", DateTime, nullable=True)
    reference_table = Column("RFRNC_TBL", String, nullable=True) # Needs to be a table with a relation(parent/child) to the table
    reference_column = Column("RFRNC_COL", String, nullable=True)

class MigrationDetails(Base):
    __tablename__ = "MGRT_DTLS"
    id = Column("ID", Integer, primary_key=True)
    enabled = Column("ENABLE", Boolean, nullable=False)
    db = Column("DB", String, ForeignKey('DB.NAME'))
    schema = Column("SCHEMA", String, nullable=False)

class AnonymizationDetails(Base):
    __tablename__ = "ANON_DTLS"
    id = Column("ID", Integer, primary_key=True)
    enabled = Column("ENABLE", Boolean, nullable=False)
    db = Column("DB", String, ForeignKey('DB.NAME'))
    schema = Column("SCHEMA", String, nullable=False)
    table = Column("TABLE", String, nullable=False)
    column = Column("COL", String, nullable=False)
    len = Column("LEN", Integer, nullable=True)
    pii_typ = Column("PII_TYP", String, ForeignKey("PII_TYP.TYP"))

class Processes(Base):
    __tablename__ = "PROC_LIST"
    name = Column("NAME", String, primary_key = True)
    desc = Column("DESC", String)

class DatabaseProcessStatus(Base):
    __tablename__ = "PROC_DB"
    id = Column("ID", Integer, primary_key=True)
    typ = Column(String)
    db = Column("DB", String)
    start_time = Column("START", DateTime, nullable=False)
    end_time = Column("END", DateTime)
    status = Column("STATUS", String, nullable=False)

class TableProcessStatus(Base):
    __tablename__ = "PROC_TBL"
    id = Column("ID", Integer, primary_key=True)
    proc_db = Column(Integer, ForeignKey("PROC_DB.ID"))
    table = Column("TABLE", String, nullable=False)
    start_time = Column("START", DateTime, nullable=False)
    end_time = Column("END", DateTime)
    status = Column("STATUS", String, nullable=False)

def create_all(engine : Engine):
    # if engine.dialect.name == 'sqlite':
    #     print("SQLITE detected. Setting schema to None.")
    #     Base.metadata.schema = None
    Base.metadata.create_all(engine)
    with engine.connect() as connection:
        connection.execute(insert(PiiType).values(typ="empty", desc="Null value"))