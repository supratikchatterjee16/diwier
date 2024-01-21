import json
import os
import sys
import argparse
import logging
import uvicorn
from pathlib import Path
from werkzeug.security import check_password_hash, generate_password_hash

from diweir.actions.anonymization import anonymize
from diweir.config import AnonymizationConfiguration, ServerConfiguration, default_conf
from diweir.utils import get_app_location
from diweir.server import start_server

app_loc = get_app_location()

# initiate logger
logger = logging.getLogger()
formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s")
stdoutHandler = logging.StreamHandler(sys.stdout)
stdoutHandler.setLevel(logging.DEBUG)
stdoutHandler.setFormatter(formatter)
logger.addHandler(stdoutHandler)

config_loc = Path(os.path.join(app_loc, 'conf', 'diweir-config.json'))
if not os.path.exists(config_loc.absolute()):
    try:
        os.makedirs(config_loc.parent.absolute())
    except:
        pass
    with open(config_loc.absolute(), 'w') as config_file:
        json.dump(default_conf, config_file)
    logger.info(f"Log file created at {config_loc.absolute()}")

with open(config_loc.absolute(), 'r') as config_file:
    common_config = json.load(config_file)

# creating parser object
class ArgsParser(argparse.ArgumentParser):
    def error(self, message):# Modified to show help text on error
        sys.stderr.write('\033[0;31merror: %s\n\n\033[0m' % message)
        self.print_help()
        sys.exit(2)

# def execute(script_type, source, destination=None, tables=None):
#     if script_type == 'purge':
#         if tables is not None and len(tables) > 0:
#             prepare_purge(create_engine(source), tables)
#     elif script_type == 'backup':
#         prepare_backup(create_engine(source), tables)
#     else :
#         print('No such options exist')
#         sys.exit(1)
#     pass

def run():
    parser = ArgsParser()
    subparser = parser.add_subparsers(title="commands", dest="command")

    # Subparsers for action
    purging_subparser = subparser.add_parser("purge", help="Purge the data held within ")
    purging_subparser.add_argument('--meta',       required = False,    nargs=1, help='Metadata DB URL', default=common_config['META_DB_URI']) # dialect://username:password@host:port/extensions
    purging_subparser.add_argument('-s', '--source',       required = True,    nargs=1, help='Source DB URL') # dialect://username:password@host:port/extensions
    purging_subparser.add_argument('-d', '--destination',  required = True,    nargs=1, help='Destination DB URL') # dialect+driver://username:password@host:port/?service_name=service
    purging_subparser.add_argument('-m', '--module',       required = True,    nargs=1, help='Schema/Owner for the tables if any.', default="public")
    purging_subparser.add_argument('--tables',             required = False,   nargs=1, help='Tables for which the solution needs to be prepared')

    purge_no_backup_subparser = subparser.add_parser("purge-no-backup", help="Purge without taking a backup")
    purge_no_backup_subparser.add_argument('--meta',       required = False,    nargs=1, help='Metadata DB URL', default=common_config['META_DB_URI']) # dialect://username:password@host:port/extensions
    purge_no_backup_subparser.add_argument('-s', '--source',       required = True,    nargs=1, help='Source DB URL') # dialect://username:password@host:port/extensions
    purge_no_backup_subparser.add_argument('-m', '--module',       required = True,    nargs=1, help='Module name to prepend to the tables to specify schema')
    purge_no_backup_subparser.add_argument('--tables',             required = False,   nargs=1, help='Tables for which the solution needs to be prepared')

    backup_subparser = subparser.add_parser("backup", help="Backup the tables defined from the frotend")
    backup_subparser.add_argument('--meta',       required = False,    nargs=1, help='Metadata DB URL', default=common_config['META_DB_URI']) # dialect://username:password@host:port/extensions
    backup_subparser.add_argument('-s', '--source',       required = True,    nargs=1, help='Source DB URL') # dialect://username:password@host:port/extensions
    backup_subparser.add_argument('-d', '--destination',  required = True,    nargs=1, help='Destination DB URL') # dialect+driver://username:password@host:port/?service_name=service
    backup_subparser.add_argument('-m', '--module',       required = True,    nargs=1, help='Schema/Owner for the tables if any.', default="public")
    backup_subparser.add_argument('--tables',             required = False,   nargs=1, help='Tables for which the solution needs to be prepared')

    migrate_subparser = subparser.add_parser("migrate", help="Migrate data between 2 databases.")
    migrate_subparser.add_argument('--meta',       required = False,    nargs=1, help='Metadata DB URL', default=common_config['META_DB_URI']) # dialect://username:password@host:port/extensions
    migrate_subparser.add_argument('-s', '--source',       required = True,    nargs=1, help='Source DB URL') # dialect://username:password@host:port/extensions
    migrate_subparser.add_argument('-d', '--destination',  required = True,    nargs=1, help='Destination DB URL') # dialect+driver://username:password@host:port/?service_name=service
    migrate_subparser.add_argument('-m', '--module',       required = True,    nargs=1, help='Schema/Owner for the tables if any.', default="public")

    anonymize_subparser = subparser.add_parser("anonymize", help="Anonymize data, as defined on the frontend.")
    anonymize_subparser.add_argument('--meta',                  required = False,   nargs=1,    help='Metadata DB URL', default=common_config['META_DB_URI']) # dialect://username:password@host:port/extensions
    anonymize_subparser.add_argument('-m', '--module',          required = True,    nargs=1,    help='Schema/Owner for the tables if any.', default="public")
    anonymize_subparser.add_argument('--fetch-size',             required = False,  nargs=1,    help='Fetch size for number of records to fetch', type=int, default=150000)
    anonymize_subparser.add_argument('--commit-size',           required = False,   nargs=1,    help='Rows to commit at a single go.', default=250000)
    anonymize_subparser.add_argument('-f', '--force',           required = False,               help='Force execute. Use when there are no running processes', action='store_true')

    server_subparser = subparser.add_parser("server", help="Start the server with specified configurations.")
    server_subparser.add_argument('--meta',                  required = False,   nargs=1,    help='Metadata DB URL', default=common_config['META_DB_URI']) # dialect://username:password@host:port/extensions
    server_subparser.add_argument('--host',             required=False, help="Specify the host. Default : 127.0.0.1",   type=str, default=common_config['SERVER_HOST'])
    server_subparser.add_argument('-p', '--port',       required=False, help="Host port",                               type=int, default=common_config['SERVER_PORT'])
    server_subparser.add_argument('-w', '--workers',    required=False, help="Specify the number of workers to use",    type=int, default=common_config['SERVER_WORKERS'])

    # Options for configurations
    password_subparser = subparser.add_parser("password", help="Change password.")
    password_subparser.add_argument('-n', '--new', required=True, help="New password to use. CAUTION : Does not cross verify.", type=str)
    password_subparser.add_argument('-o', '--old', required=True, help="Old password. Default : diweir", type=str, default="diwier")

    meta_subparser = subparser.add_parser("metadata", help="Change the easy connect string for metadata loading.")
    meta_subparser.add_argument('-n', '--new', required=True, help="New connection string to utilize", type=str)

    # script_types = {'purge', 'purge-no-backup', 'backup', 'migrate'}
    args = parser.parse_args()
    
    if args.command == 'server':
        start_server(args)
          
    if args.command == 'anonymize':
        config = AnonymizationConfiguration(args)
        anonymize(config)
    
    if args.command == 'purge':
        pass

    if args.command == 'password':
        if check_password_hash(common_config['SERVER_ADMIN_PASSWORD'], args.old):
            common_config['SERVER_ADMIN_PASSWORD'] = generate_password_hash(args.new, 'scrypt')
            with open(config_loc.absolute(), 'r') as config_file:
                json.dump(default_conf, config_file)
    
    if args.command == 'metadata':
        common_config['META_DB_URI'] = args.new
        with open(config_loc.absolute(), 'r') as config_file:
            json.dump(default_conf, config_file)
    
    # parser.print_help()