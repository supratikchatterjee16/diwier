import sqlalchemy

class RdbmsConnection:
    def __init__(self, config):
        self._conn_str = config.connection
        if hasattr(config, 'fetch_size'):
            self._fetch_size = config.fetch_size
        if hasattr(config, 'commit_size'):
            self._commit_size = config.commit_size
        self._current_conn = None
        self._engine = None

    @property
    def engine(self) -> sqlalchemy.Engine:
        if self._engine is None:
            self._engine = sqlalchemy.create_engine(self._conn_str)
        return self._engine

    def __enter__(self):
        conn = None
        try :
            conn = self.engine.raw_connection()
        except:
            pass
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
