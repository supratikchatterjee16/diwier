import logging
import sqlalchemy
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger()

class RdbmsConnection:
    """
    The base connection object for maintaining connectios and working with them.
    Uses SQLAlchemy to provide multiple DB support.
    """

    def __init__(self, config):
        self._conn_str = config.connection
        if hasattr(config, "fetch_size"):
            self._fetch_size = config.fetch_size
        if hasattr(config, "commit_size"):
            self._commit_size = config.commit_size
        self._current_conn = None
        self._engine = None
        self._session_maker = None

    @property
    def engine(self) -> sqlalchemy.Engine:
        if self._engine is None:
            self._engine = sqlalchemy.create_engine(
                self._conn_str,
                pool_size=20,
                max_overflow=10,
                pool_timeout=30,
                pool_recycle=1000,
            )
        return self._engine

    def create_session(self):
        if self._session_maker is None :
            self._session_maker = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        session = self._session_maker()
        try :
            yield session
        finally:
            session.close()
    
    def __enter__(self):
        conn = None
        try:
            conn = self.engine.raw_connection()
        except sqlalchemy.SQLAlchemyError as e:
            logger.error("An error occured while attempting to connect : ")
            logger.error(e)
        self._current_conn = conn
        return self._current_conn.cursor()

    def __exit__(self, exc_typ, exc_val, exc_tb):
        self._current_conn.close()


class MetadataConnection(RdbmsConnection):
    def __init__(self, config):
        super().__init__(config)


class ExternalConnection(RdbmsConnection):
    def __init__(self, config):
        super().__init__(config)
        self._config = config

    def clone(self):
        return ExternalConnection(self._config)
