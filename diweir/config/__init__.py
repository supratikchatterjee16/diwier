
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
    #  'SERVER_ADMIN_PASSWORD' : generate_password_hash('diweir', 'scrypt'),
}

class ServerConfiguration:
    def __init__(self, args):
        if args.host :
            self.host = args.host
        else :
            self.host = default_conf['SERVER_HOST']
        if args.port :
            self.port = args.port
        else :
            self.port = default_conf['SERVER_PORT']
        if args.workers:
            self.workers = args.workers
        else :
            self.workers = default_conf['SERVER_WORKERS']
        if args.meta :
            self.connection = args.meta
        else :
            self.connection = default_conf['META_DB_URI']
        
        
        self._conn : MetadataConnection = MetadataConnection(self)
    
    def get_conn(self) -> MetadataConnection:
        return self._conn

class AnonymizationConfiguration:
    def __init__(self, args):
        # Placeholder for Anonymization configurations
        pass

class PurgeConfiguration:
    def __init__(self):
        # Placeholder for Purge configurations
        pass