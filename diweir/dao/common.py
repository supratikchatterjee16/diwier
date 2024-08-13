from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, insert
from sqlalchemy.orm import mapped_column, Mapped
from diweir.dao import Base

from datetime import datetime

class DBProvider(Base):
    __tablename__ = "DB_PRVDR"
    provider = Column("PRVDR", String, primary_key=True)
    name = Column("NAME", String, unique=True)

class Environment(Base):
    __tablename__ = "ENV"
    name = Column("NAME", String, primary_key = True)
    desc = Column("DSCRB", String)
    created_on = Column('CREATED_ON', DateTime, nullable=False, default=datetime.now())
    modified_on = Column('MODIFIED_ON', DateTime, nullable=False, default=datetime.now())
    created_by = Column('CREATED_BY', String, nullable=False)
    modified_by = Column('MODIFIED_BY', String, nullable=False)

class Databases(Base):
    __tablename__ = "DB"
    id = Column('ID', Integer, primary_key=True)
    name = Column("NAME", String)
    env : Mapped[str] = mapped_column("ENV", ForeignKey(Environment.name))
    provider : Mapped[str] = mapped_column("PVDR", ForeignKey(DBProvider.provider))
    username = Column("USER", String, nullable=False)
    password = Column("PWD", String, nullable=False)
    host = Column("HOST", String, nullable=False)
    port = Column("PORT", Integer, nullable=False)
    schema = Column("SCHEMA", String, nullable=False)
    created_on = Column('CREATED_ON', DateTime, nullable=False, default=datetime.now())
    modified_on = Column('MODIFIED_ON', DateTime, nullable=False, default=datetime.now())
    created_by = Column('CREATED_BY', String, nullable=False)
    modified_by = Column('MODIFIED_BY', String, nullable=False)

class ColumnInformation(Base):
    __tablename__ = 'COL_INFO'
    id = Column('ID', Integer, primary_key = True)
    db = mapped_column('DB_ID', ForeignKey('DB.ID'))
    table = Column('TAB', String, nullable=False)
    column = Column('COL', String, nullable=False)
    created_on = Column('CREATED_ON', DateTime, nullable=False, default=datetime.now())
    modified_on = Column('MODIFIED_ON', DateTime, nullable=False, default=datetime.now())
    created_by = Column('CREATED_BY', String, nullable=False)
    modified_by = Column('MODIFIED_BY', String, nullable=False)

class TaskType(Base):
    __tablename__= 'TASK_TYPE'
    id = Column('ID', Integer, primary_key = True)
    task_name = Column('NAME', String, unique=True, nullable=False)
    task_desc = Column('DESC', String, nullable=False)

class Task(Base):
    __tablename__ = 'TASK'
    id = Column('ID', Integer, primary_key = True)
    type = mapped_column('TYPE', ForeignKey(TaskType.id))
    name = Column('NAME', String, nullable = False)
    created_on = Column('CREATED_ON', DateTime, nullable=False, default=datetime.now())
    modified_on = Column('MODIFIED_ON', DateTime, nullable=False, default=datetime.now())
    created_by = Column('CREATED_BY', String, nullable=False)
    modified_by = Column('MODIFIED_BY', String, nullable=False)

class TaskGroup(Base):
    __tablename__ = 'TASK_GROUP'
    id = Column('ID', Integer, primary_key=True)
    type = mapped_column('TYPE', ForeignKey('TASK_TYPE.ID'))
    name = Column('NAME', String, nullable=False)
    task_id = mapped_column('TASK_ID', ForeignKey('TASK.ID'))
    created_on = Column('CREATED_ON', DateTime, nullable=False, default=datetime.now())
    modified_on = Column('MODIFIED_ON', DateTime, nullable=False, default=datetime.now())
    created_by = Column('CREATED_BY', String, nullable=False)
    modified_by = Column('MODIFIED_BY', String, nullable=False)

class TaskColumnMappping(Base):
    __tablename__ = 'TASK_COL_MAP'
    id = Column('ID', Integer, primary_key = True)
    task_id = mapped_column('TASK_ID', ForeignKey('TASK_TYPE.ID'))
    column_info = mapped_column('COL_ID', ForeignKey('COL_INFO.ID'))
    created_on = Column('CREATED_ON', DateTime, nullable=False, default=datetime.now())
    modified_on = Column('MODIFIED_ON', DateTime, nullable=False, default=datetime.now())
    created_by = Column('CREATED_BY', String, nullable=False)
    modified_by = Column('MODIFIED_BY', String, nullable=False)

class Roles(Base):
    __tablename__ = 'ROLE'
    id = Column('ID', Integer, primary_key = True)
    name = Column('NAME', String, nullable=False, unique=True)
    description = Column('DESC', String, nullable=False)

class User(Base):
    __tablename__ = 'USER'
    id = Column('ID', Integer, primary_key = True)
    name = Column('NAME', String, unique=True, nullable=False)
    role_id = mapped_column('ROLE', ForeignKey('ROLE.ID'))
    passkey = Column('PASS', String)
    created_on = Column('CREATED_ON', DateTime, nullable=False, default=datetime.now())
    modified_on = Column('MODIFIED_ON', DateTime, nullable=False, default=datetime.now())
    created_by = Column('CREATED_BY', String, nullable=False)
    modified_by = Column('MODIFIED_BY', String, nullable=False)
