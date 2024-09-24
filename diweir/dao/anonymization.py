from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import mapped_column, Mapped, Session
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
    
    @staticmethod
    def create_pii_type(session: Session, code: str, dtype: str, description: str, options: str) -> 'PiiType':
        try:
            new_pii_type = PiiType(code=code, dtype=dtype, description=description, options=options)
            session.add(new_pii_type)
            session.commit()
            return new_pii_type
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error creating PII Type: {str(e)}")
            return None

    @staticmethod
    def get_pii_type_by_id(session: Session, pii_type_id: int) -> 'PiiType':
        try:
            pii_type = session.query(PiiType).filter_by(id=pii_type_id).first()
            return pii_type
        except SQLAlchemyError as e:
            print(f"Error retrieving PII Type: {str(e)}")
            return None

    @staticmethod
    def get_all_pii_types(session: Session) -> list['PiiType']:
        try:
            pii_types = session.query(PiiType).all()
            return pii_types
        except SQLAlchemyError as e:
            print(f"Error retrieving PII Types: {str(e)}")
            return []

    @staticmethod
    def update_pii_type(session: Session, pii_type_id: int, code: str = None, dtype: str = None, 
                        description: str = None, options: str = None) -> 'PiiType':
        try:
            pii_type = session.query(PiiType).filter_by(id=pii_type_id).first()
            if pii_type:
                if code:
                    pii_type.code = code
                if dtype:
                    pii_type.dtype = dtype
                if description:
                    pii_type.description = description
                if options:
                    pii_type.options = options
                session.commit()
            return pii_type
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error updating PII Type: {str(e)}")
            return None

    @staticmethod
    def delete_pii_type(session: Session, pii_type_id: int) -> bool:
        try:
            pii_type = session.query(PiiType).filter_by(id=pii_type_id).first()
            if pii_type:
                session.delete(pii_type)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error deleting PII Type: {str(e)}")
            return False


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

    @staticmethod
    def create_user_def(session: Session, task_id: int, column_info: int, option: str, created_by: int) -> 'AnonymizationUserDefinitions':
        try:
            new_def = AnonymizationUserDefinitions(
                task_id=task_id,
                column_info=column_info,
                option=option,
                created_by=created_by,
                modified_by=created_by
            )
            session.add(new_def)
            session.commit()
            return new_def
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error creating AnonymizationUserDefinition: {str(e)}")
            return None

    @staticmethod
    def get_user_def_by_id(session: Session, def_id: int) -> 'AnonymizationUserDefinitions':
        try:
            return session.query(AnonymizationUserDefinitions).filter_by(id=def_id).first()
        except SQLAlchemyError as e:
            print(f"Error retrieving AnonymizationUserDefinition: {str(e)}")
            return None

    @staticmethod
    def get_all_user_defs(session: Session) -> list['AnonymizationUserDefinitions']:
        try:
            return session.query(AnonymizationUserDefinitions).all()
        except SQLAlchemyError as e:
            print(f"Error retrieving AnonymizationUserDefinitions: {str(e)}")
            return []

    @staticmethod
    def update_user_def(session: Session, def_id: int, task_id: int = None, column_info: int = None,
                        option: str = None, modified_by: int = None) -> 'AnonymizationUserDefinitions':
        try:
            user_def = session.query(AnonymizationUserDefinitions).filter_by(id=def_id).first()
            if user_def:
                if task_id:
                    user_def.task_id = task_id
                if column_info:
                    user_def.column_info = column_info
                if option:
                    user_def.option = option
                if modified_by:
                    user_def.modified_by = modified_by
                session.commit()
            return user_def
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error updating AnonymizationUserDefinition: {str(e)}")
            return None

    @staticmethod
    def delete_user_def(session: Session, def_id: int) -> bool:
        try:
            user_def = session.query(AnonymizationUserDefinitions).filter_by(id=def_id).first()
            if user_def:
                session.delete(user_def)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error deleting AnonymizationUserDefinition: {str(e)}")
            return False