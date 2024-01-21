
import os
from diweir.utils.connections import MetadataConnection
from werkzeug.security import generate_password_hash

from diweir.utils import get_app_location


app_loc = get_app_location()
default_db = os.path.join(app_loc, 'meta.db')

default_conf = {
     'META_DB_URI' : f'sqlite:///{default_db}',
     'SERVER_HOST' : '127.0.0.1',
     'SERVER_PORT' : 1232,
     'SERVER_WORKERS' : 4,
     'SERVER_ADMIN_PASSWORD' : generate_password_hash('diweir', 'scrypt'),
}

class ServerConfiguration:
    def __init__(self, args):
        self.host = args.host
        self.port = args.port
        self.workers = args.port
        self.connection = args.meta
        self._conn = MetadataConnection(self)
    
    def get_conn(self):
        return self._conn

class AnonymizationConfiguration:
    def __init__(self, args):
        pass