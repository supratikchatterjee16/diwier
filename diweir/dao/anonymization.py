from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from diweir.dao import Base

from .common import Task, ColumnInformation, User

class PiiType(Base):
    '''
    This is the defintion table for PII Types supported by the utility.
    '''
    __tablename__ = 'PII_TYPE'
    id = Column('ID', Integer, primary_key=True)
    code =  Column('CODE', String(5))
    dtype = Column('DTYPE', String(10))
    description = Column('DESCR', String(25))
    options = Column('OPTIONS', String(10))

class AnonymizationUserDefinitions(Base):
    __tablename__ = 'ANON_USER_DEFN'
    id = Column('ID', Integer, primary_key=True)
    task_id : Mapped[int]= mapped_column('TASK_ID', ForeignKey(Task.id))
    column_info : Mapped[int] = mapped_column('COL_INFO_ID', ForeignKey(ColumnInformation.id))
    option = Column('OPTION', String(5))
    created_on = Column('CREATED_ON', DateTime)
    modified_on = Column('MODIFIED_ON', DateTime)
    created_by : Mapped[int] = mapped_column('CREATED_BY', ForeignKey(User.id))
    modified_by : Mapped[int] = mapped_column('MODIFIED_BY', ForeignKey(User.id))