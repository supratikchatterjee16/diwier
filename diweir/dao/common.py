from diweir.dto import DatabaseDto, EnvironmentDto
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, insert
from sqlalchemy.orm import mapped_column, Mapped, Session
from diweir.dao import Base

from datetime import datetime


class DBProvider(Base):
    __tablename__ = "DB_PRVDR"
    provider = Column("PRVDR", String, primary_key=True)
    name = Column("NAME", String, unique=True)


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


class TaskType(Base):
    __tablename__ = "TASK_TYPE"
    id = Column("ID", Integer, primary_key=True)
    task_name = Column("NAME", String, unique=True, nullable=False)
    task_desc = Column("DESC", String, nullable=False)


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


class TaskColumnMappping(Base):
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


class Roles(Base):
    __tablename__ = "ROLE"
    id = Column("ID", Integer, primary_key=True)
    name = Column("NAME", String, nullable=False, unique=True)
    description = Column("DESC", String, nullable=False)


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
