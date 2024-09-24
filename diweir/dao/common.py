from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import mapped_column, Mapped, Session

from diweir.dao import Base
from diweir.dto import DatabaseDto, EnvironmentDto

class DBProvider(Base):
    __tablename__ = "DB_PRVDR"
    
    provider = Column("PRVDR", String, primary_key=True)
    name = Column("NAME", String, unique=True)

    @staticmethod
    def create_db_provider(session: Session, provider: str, name: str) -> 'DBProvider':
        try:
            new_provider = DBProvider(provider=provider, name=name)
            session.add(new_provider)
            session.commit()
            return new_provider
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error creating DBProvider: {str(e)}")
            return None

    @staticmethod
    def get_db_provider_by_provider(session: Session, provider: str) -> 'DBProvider':
        try:
            return session.query(DBProvider).filter_by(provider=provider).first()
        except SQLAlchemyError as e:
            print(f"Error retrieving DBProvider: {str(e)}")
            return None

    @staticmethod
    def get_all_db_providers(session: Session) -> list['DBProvider']:
        try:
            return session.query(DBProvider).all()
        except SQLAlchemyError as e:
            print(f"Error retrieving DBProvider records: {str(e)}")
            return []

    @staticmethod
    def update_db_provider(session: Session, provider: str, name: str = None) -> 'DBProvider':
        try:
            db_provider = session.query(DBProvider).filter_by(provider=provider).first()
            if db_provider:
                if name:
                    db_provider.name = name
                session.commit()
            return db_provider
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error updating DBProvider: {str(e)}")
            return None

    @staticmethod
    def delete_db_provider(session: Session, provider: str) -> bool:
        try:
            db_provider = session.query(DBProvider).filter_by(provider=provider).first()
            if db_provider:
                session.delete(db_provider)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error deleting DBProvider: {str(e)}")
            return False


class Environment(Base):
    __tablename__ = "ENV"
    name = Column("NAME", String, primary_key=True)
    desc = Column("DSCRB", String)
    created_on = Column("CREATED_ON", DateTime, nullable=False, default=datetime.now())
    modified_on = Column(
        "MODIFIED_ON", DateTime, nullable=False, default=datetime.now()
    )
    created_by = Column("CREATED_BY", String, nullable=False)
    modified_by = Column("MODIFIED_BY", String, nullable=False)

    def __init__(self, env: EnvironmentDto = None, **kwargs):
        super().__init__(**kwargs)
        if env:
            self.name = env.name
            self.desc = env.desc
            self.created_on = datetime.now()
            self.modified_on = datetime.now()
            # TODO : Change user add logic to something else
            self.created_by = "admin"
            self.modified_by = "admin"

    def update(self, database: EnvironmentDto):
        for attr in vars(database).keys():
            original = getattr(self, attr)
            required = getattr(database, attr)
            if original != required:
                setattr(self, attr, required)
    
    @staticmethod
    def create(session: Session, environment: EnvironmentDto):
        entry = Environment(env=environment)
        session.add(entry)
        session.commit()
        session.refresh(entry)
        return entry

    @staticmethod
    def update(session: Session, environment: EnvironmentDto):
        entry = session.query(Environment).filter(Environment.name == environment.name).first()
        if entry:
            entry.update(environment)
            session.commit()
            session.refresh(entry)
        return entry

    @staticmethod
    def delete(session: Session, environment: EnvironmentDto):
        entry = session.query(Environment).filter(Environment.name == environment.name).first()
        if entry:
            session.delete(entry)
            session.commit()
        return entry

    @staticmethod
    def get_all(session: Session, skip: int = 0, limit: int = 50):
        return session.query(Environment).offset(skip).limit(limit).all()

    @staticmethod
    def get(session: Session, name: str):
        return session.query(Environment).filter(Environment.name == name).first()


class Databases(Base):
    __tablename__ = "DB"
    id = Column("ID", Integer, primary_key=True)
    name = Column("NAME", String)
    env: Mapped[str] = mapped_column("ENV", ForeignKey(Environment.name))
    provider: Mapped[str] = mapped_column("PVDR", ForeignKey(DBProvider.provider))
    username = Column("USER", String, nullable=False)
    password = Column("PWD", String, nullable=False)
    host = Column("HOST", String, nullable=False)
    port = Column("PORT", Integer, nullable=False)
    schm = Column("SCHEMA", String, nullable=False)
    created_on = Column("CREATED_ON", DateTime, nullable=False, default=datetime.now())
    modified_on = Column(
        "MODIFIED_ON", DateTime, nullable=False, default=datetime.now()
    )
    created_by = Column("CREATED_BY", String, nullable=False)
    modified_by = Column("MODIFIED_BY", String, nullable=False)

    def __init__(self, db_data: DatabaseDto = None, **kwargs):
        super.__init__(**kwargs)
        if db_data:
            self.name = db_data.name
            self.env = db_data.env
            self.provider = db_data.prvdr
            self.username = db_data.user
            # TODO : Encrypt the following
            self.password = db_data.psk
            self.host = db_data.host
            self.port = db_data.port
            self.schm = db_data.schm
            self.created_on = datetime.now()
            self.modified_on = datetime.now()
            # TODO : Change user add logic to something else
            self.created_by = "admin"
            self.modified_by = "admin"

    def update(self, database: DatabaseDto):
        for attr in vars(database).keys():
            original = getattr(self, attr)
            required = getattr(database, attr)
            if original != required:
                setattr(self, attr, required)

    @staticmethod
    def create(session: Session, database: DatabaseDto):
        entry = Databases(db_data=database)
        session.add(entry)
        session.commit()
        session.refresh(entry)
        return entry

    @staticmethod
    def update(session: Session, database: DatabaseDto):
        entry = session.query(Databases).filter(Databases.name == database.name).first()
        if entry:
            entry.update(database)
            session.commit()
            session.refresh(entry)
        return entry

    @staticmethod
    def delete(session: Session, database: DatabaseDto):
        entry = session.query(Databases).filter(Databases.name == database.name).first()
        if entry:
            session.delete(entry)
            session.commit()
        return entry

    @staticmethod
    def get_all(session: Session, skip: int = 0, limit: int = 50):
        return session.query(Databases).offset(skip).limit(limit).all()

    @staticmethod
    def get(session: Session, name: str):
        return session.query(Databases).filter(Databases.name == name).first()


class ColumnInformation(Base):
    __tablename__ = "COL_INFO"
    id = Column("ID", Integer, primary_key=True)
    db = mapped_column("DB_ID", ForeignKey("DB.ID"))
    table = Column("TAB", String, nullable=False)
    column = Column("COL", String, nullable=False)
    created_on = Column("CREATED_ON", DateTime, nullable=False, default=datetime.now())
    modified_on = Column(
        "MODIFIED_ON", DateTime, nullable=False, default=datetime.now()
    )
    created_by = Column("CREATED_BY", String, nullable=False)
    modified_by = Column("MODIFIED_BY", String, nullable=False)

    @staticmethod
    def create_column_info(session: Session, db_id: int, table: str, column: str, created_by: str) -> 'ColumnInformation':
        try:
            new_info = ColumnInformation(db=db_id, table=table, column=column, created_by=created_by, modified_by=created_by)
            session.add(new_info)
            session.commit()
            return new_info
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error creating ColumnInformation: {str(e)}")
            return None

    @staticmethod
    def get_column_info_by_id(session: Session, info_id: int) -> 'ColumnInformation':
        try:
            return session.query(ColumnInformation).filter_by(id=info_id).first()
        except SQLAlchemyError as e:
            print(f"Error retrieving ColumnInformation: {str(e)}")
            return None

    @staticmethod
    def get_all_column_infos(session: Session) -> list['ColumnInformation']:
        try:
            return session.query(ColumnInformation).all()
        except SQLAlchemyError as e:
            print(f"Error retrieving ColumnInformation records: {str(e)}")
            return []

    @staticmethod
    def update_column_info(session: Session, info_id: int, table: str = None, column: str = None, modified_by: str = None) -> 'ColumnInformation':
        try:
            info = session.query(ColumnInformation).filter_by(id=info_id).first()
            if info:
                if table:
                    info.table = table
                if column:
                    info.column = column
                if modified_by:
                    info.modified_by = modified_by
                session.commit()
            return info
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error updating ColumnInformation: {str(e)}")
            return None

    @staticmethod
    def delete_column_info(session: Session, info_id: int) -> bool:
        try:
            info = session.query(ColumnInformation).filter_by(id=info_id).first()
            if info:
                session.delete(info)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error deleting ColumnInformation: {str(e)}")
            return False


class TaskType(Base):
    __tablename__ = "TASK_TYPE"
    id = Column("ID", Integer, primary_key=True)
    task_name = Column("NAME", String, unique=True, nullable=False)
    task_desc = Column("DESC", String, nullable=False)

    @staticmethod
    def create_task_type(session: Session, task_name: str, task_desc: str) -> 'TaskType':
        try:
            new_task_type = TaskType(task_name=task_name, task_desc=task_desc)
            session.add(new_task_type)
            session.commit()
            return new_task_type
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error creating TaskType: {str(e)}")
            return None

    @staticmethod
    def get_task_type_by_id(session: Session, task_type_id: int) -> 'TaskType':
        try:
            return session.query(TaskType).filter_by(id=task_type_id).first()
        except SQLAlchemyError as e:
            print(f"Error retrieving TaskType: {str(e)}")
            return None

    @staticmethod
    def get_all_task_types(session: Session) -> list['TaskType']:
        try:
            return session.query(TaskType).all()
        except SQLAlchemyError as e:
            print(f"Error retrieving TaskType records: {str(e)}")
            return []

    @staticmethod
    def update_task_type(session: Session, task_type_id: int, task_name: str = None, task_desc: str = None) -> 'TaskType':
        try:
            task_type = session.query(TaskType).filter_by(id=task_type_id).first()
            if task_type:
                if task_name:
                    task_type.task_name = task_name
                if task_desc:
                    task_type.task_desc = task_desc
                session.commit()
            return task_type
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error updating TaskType: {str(e)}")
            return None

    @staticmethod
    def delete_task_type(session: Session, task_type_id: int) -> bool:
        try:
            task_type = session.query(TaskType).filter_by(id=task_type_id).first()
            if task_type:
                session.delete(task_type)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error deleting TaskType: {str(e)}")
            return False


class Task(Base):
    __tablename__ = "TASK"
    id = Column("ID", Integer, primary_key=True)
    type = mapped_column("TYPE", ForeignKey(TaskType.id))
    name = Column("NAME", String, nullable=False)
    created_on = Column("CREATED_ON", DateTime, nullable=False, default=datetime.now())
    modified_on = Column(
        "MODIFIED_ON", DateTime, nullable=False, default=datetime.now()
    )
    created_by = Column("CREATED_BY", String, nullable=False)
    modified_by = Column("MODIFIED_BY", String, nullable=False)

    @staticmethod
    def create_task(session: Session, task_type_id: int, name: str, created_by: str) -> 'Task':
        try:
            new_task = Task(type=task_type_id, name=name, created_by=created_by, modified_by=created_by)
            session.add(new_task)
            session.commit()
            return new_task
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error creating Task: {str(e)}")
            return None

    @staticmethod
    def get_task_by_id(session: Session, task_id: int) -> 'Task':
        try:
            return session.query(Task).filter_by(id=task_id).first()
        except SQLAlchemyError as e:
            print(f"Error retrieving Task: {str(e)}")
            return None

    @staticmethod
    def get_all_tasks(session: Session) -> list['Task']:
        try:
            return session.query(Task).all()
        except SQLAlchemyError as e:
            print(f"Error retrieving Task records: {str(e)}")
            return []

    @staticmethod
    def update_task(session: Session, task_id: int, name: str = None, task_type_id: int = None, modified_by: str = None) -> 'Task':
        try:
            task = session.query(Task).filter_by(id=task_id).first()
            if task:
                if name:
                    task.name = name
                if task_type_id:
                    task.type = task_type_id
                if modified_by:
                    task.modified_by = modified_by
                session.commit()
            return task
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error updating Task: {str(e)}")
            return None

    @staticmethod
    def delete_task(session: Session, task_id: int) -> bool:
        try:
            task = session.query(Task).filter_by(id=task_id).first()
            if task:
                session.delete(task)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error deleting Task: {str(e)}")
            return False

class TaskGroup(Base):
    __tablename__ = "TASK_GROUP"
    id = Column("ID", Integer, primary_key=True)
    type = mapped_column("TYPE", ForeignKey("TASK_TYPE.ID"))
    name = Column("NAME", String, nullable=False)
    task_id = mapped_column("TASK_ID", ForeignKey("TASK.ID"))
    created_on = Column("CREATED_ON", DateTime, nullable=False, default=datetime.now())
    modified_on = Column(
        "MODIFIED_ON", DateTime, nullable=False, default=datetime.now()
    )
    created_by = Column("CREATED_BY", String, nullable=False)
    modified_by = Column("MODIFIED_BY", String, nullable=False)

    @staticmethod
    def create_task_group(session: Session, task_type_id: int, task_id: int, name: str, created_by: str) -> 'TaskGroup':
        try:
            new_group = TaskGroup(type=task_type_id, task_id=task_id, name=name, created_by=created_by, modified_by=created_by)
            session.add(new_group)
            session.commit()
            return new_group
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error creating TaskGroup: {str(e)}")
            return None

    @staticmethod
    def get_task_group_by_id(session: Session, group_id: int) -> 'TaskGroup':
        try:
            return session.query(TaskGroup).filter_by(id=group_id).first()
        except SQLAlchemyError as e:
            print(f"Error retrieving TaskGroup: {str(e)}")
            return None

    @staticmethod
    def get_all_task_groups(session: Session) -> list['TaskGroup']:
        try:
            return session.query(TaskGroup).all()
        except SQLAlchemyError as e:
            print(f"Error retrieving TaskGroup records: {str(e)}")
            return []

    @staticmethod
    def update_task_group(session: Session, group_id: int, name: str = None, task_type_id: int = None, modified_by: str = None) -> 'TaskGroup':
        try:
            group = session.query(TaskGroup).filter_by(id=group_id).first()
            if group:
                if name:
                    group.name = name
                if task_type_id:
                    group.type = task_type_id
                if modified_by:
                    group.modified_by = modified_by
                session.commit()
            return group
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error updating TaskGroup: {str(e)}")
            return None

    @staticmethod
    def delete_task_group(session: Session, group_id: int) -> bool:
        try:
            group = session.query(TaskGroup).filter_by(id=group_id).first()
            if group:
                session.delete(group)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error deleting TaskGroup: {str(e)}")
            return False


class TaskColumnMapping(Base):
    __tablename__ = "TASK_COL_MAP"
    id = Column("ID", Integer, primary_key=True)
    task_id = mapped_column("TASK_ID", ForeignKey("TASK_TYPE.ID"))
    column_info = mapped_column("COL_ID", ForeignKey("COL_INFO.ID"))
    created_on = Column("CREATED_ON", DateTime, nullable=False, default=datetime.now())
    modified_on = Column(
        "MODIFIED_ON", DateTime, nullable=False, default=datetime.now()
    )
    created_by = Column("CREATED_BY", String, nullable=False)
    modified_by = Column("MODIFIED_BY", String, nullable=False)

    @staticmethod
    def create_task_column_mapping(session: Session, task_id: int, column_info_id: int, created_by: str) -> 'TaskColumnMapping':
        try:
            new_mapping = TaskColumnMapping(task_id=task_id, column_info=column_info_id, created_by=created_by, modified_by=created_by)
            session.add(new_mapping)
            session.commit()
            return new_mapping
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error creating TaskColumnMapping: {str(e)}")
            return None

    @staticmethod
    def get_task_column_mapping_by_id(session: Session, mapping_id: int) -> 'TaskColumnMapping':
        try:
            return session.query(TaskColumnMapping).filter_by(id=mapping_id).first()
        except SQLAlchemyError as e:
            print(f"Error retrieving TaskColumnMapping: {str(e)}")
            return None

    @staticmethod
    def get_all_task_column_mappings(session: Session) -> list['TaskColumnMapping']:
        try:
            return session.query(TaskColumnMapping).all()
        except SQLAlchemyError as e:
            print(f"Error retrieving TaskColumnMapping records: {str(e)}")
            return []

    @staticmethod
    def update_task_column_mapping(session: Session, mapping_id: int, task_id: int = None, column_info_id: int = None, modified_by: str = None) -> 'TaskColumnMapping':
        try:
            mapping = session.query(TaskColumnMapping).filter_by(id=mapping_id).first()
            if mapping:
                if task_id:
                    mapping.task_id = task_id
                if column_info_id:
                    mapping.column_info = column_info_id
                if modified_by:
                    mapping.modified_by = modified_by
                session.commit()
            return mapping
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error updating TaskColumnMapping: {str(e)}")
            return None

    @staticmethod
    def delete_task_column_mapping(session: Session, mapping_id: int) -> bool:
        try:
            mapping = session.query(TaskColumnMapping).filter_by(id=mapping_id).first()
            if mapping:
                session.delete(mapping)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error deleting TaskColumnMapping: {str(e)}")
            return False


class Roles(Base):
    __tablename__ = "ROLE"
    id = Column("ID", Integer, primary_key=True)
    name = Column("NAME", String, nullable=False, unique=True)
    description = Column("DESC", String, nullable=False)

    @staticmethod
    def create_role(session: Session, name: str, description: str) -> 'Roles':
        try:
            new_role = Roles(name=name, description=description)
            session.add(new_role)
            session.commit()
            return new_role
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error creating Role: {str(e)}")
            return None

    @staticmethod
    def get_role_by_id(session: Session, role_id: int) -> 'Roles':
        try:
            return session.query(Roles).filter_by(id=role_id).first()
        except SQLAlchemyError as e:
            print(f"Error retrieving Role: {str(e)}")
            return None

    @staticmethod
    def get_all_roles(session: Session) -> list['Roles']:
        try:
            return session.query(Roles).all()
        except SQLAlchemyError as e:
            print(f"Error retrieving Roles records: {str(e)}")
            return []

    @staticmethod
    def update_role(session: Session, role_id: int, name: str = None, description: str = None) -> 'Roles':
        try:
            role = session.query(Roles).filter_by(id=role_id).first()
            if role:
                if name:
                    role.name = name
                if description:
                    role.description = description
                session.commit()
            return role
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error updating Role: {str(e)}")
            return None

    @staticmethod
    def delete_role(session: Session, role_id: int) -> bool:
        try:
            role = session.query(Roles).filter_by(id=role_id).first()
            if role:
                session.delete(role)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error deleting Role: {str(e)}")
            return False


class User(Base):
    __tablename__ = "USER"
    id = Column("ID", Integer, primary_key=True)
    name = Column("NAME", String, unique=True, nullable=False)
    role_id = mapped_column("ROLE", ForeignKey("ROLE.ID"))
    passkey = Column("PASS", String)
    created_on = Column("CREATED_ON", DateTime, nullable=False, default=datetime.now())
    modified_on = Column(
        "MODIFIED_ON", DateTime, nullable=False, default=datetime.now()
    )
    created_by = Column("CREATED_BY", String, nullable=False)
    modified_by = Column("MODIFIED_BY", String, nullable=False)

    @staticmethod
    def create_user(session: Session, name: str, role_id: int, passkey: str, created_by: str) -> 'User':
        try:
            new_user = User(name=name, role_id=role_id, passkey=passkey, created_by=created_by, modified_by=created_by)
            session.add(new_user)
            session.commit()
            return new_user
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error creating User: {str(e)}")
            return None

    @staticmethod
    def get_user_by_id(session: Session, user_id: int) -> 'User':
        try:
            return session.query(User).filter_by(id=user_id).first()
        except SQLAlchemyError as e:
            print(f"Error retrieving User: {str(e)}")
            return None

    @staticmethod
    def get_all_users(session: Session) -> list['User']:
        try:
            return session.query(User).all()
        except SQLAlchemyError as e:
            print(f"Error retrieving User records: {str(e)}")
            return []

    @staticmethod
    def update_user(session: Session, user_id: int, name: str = None, role_id: int = None, passkey: str = None, modified_by: str = None) -> 'User':
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                if name:
                    user.name = name
                if role_id:
                    user.role_id = role_id
                if passkey:
                    user.passkey = passkey
                if modified_by:
                    user.modified_by = modified_by
                session.commit()
            return user
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error updating User: {str(e)}")
            return None

    @staticmethod
    def delete_user(session: Session, user_id: int) -> bool:
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                session.delete(user)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error deleting User: {str(e)}")
            return False