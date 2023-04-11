# DI-WEIR

A controlled algorithm generation mechanism for massive data operations between one or more RDBMS systems. This helps develop scripts for common 
large scale actions such as purging, backing up and migrating to another RDBMS format.

## Installation

This is `pip` installable via pypi.org.

```shell
pip install diweir
```

Additionally once the releases are available, the zip file can be downloaded and installed via : 

```shell
pip install .
```

## Usage

This can be used as a CLI or API. 

## CLI

As a CLI it requires the following : 

1. Script Type (required) : This is the type of script that needs to be prepared
2. Source (required) : A DB connection string to operate on. The dialect and engines supported can be found at [SQLAlchemy](https://docs.sqlalchemy.org/en/20/dialects/)
3. Target (optional) : A DB connection string to transfer the data to(required for migrations and backups).
4. Tables (optional) : A list of tables to be used for purging and backups. This is a list of comma separated values, without whitespaces.
5. Module (required) : The prepared may specify a module to prevent ambiguity during script execution.
6. Package Name (optional) : The program creates a PL/SQL or TSQL package for purging. The Package names set by default can be overridden using this.

## API

This can be utilized in various ways, but using this is required only in the scenario a custom solution is required.

## Status

This is a Work in Progress(WIP). As a lot of details are required to go into it, this will take some time and effort to complete.

## Contributing

Please do contribute to this however possible. We aim to provide data handling solutions to fast track data management efforts, while providing a solution that allows for full accountability during execution.

Done : 

1. Purging with backup
    1. Oracle

To-do :

1. Purging with backup
    1. PostgreSQL
    2. Redshift
    3. SQL Server 
2. Purging without backup
    1. Oracle
    2. PostgreSQL
    3. Redshift
    4. SQL Server
3. Backup
    1. Oracle
    2. PostgreSQL
    3. Redshift
    4. SQL Server
4. Migrate
    1. Oracle to SQL Server
    2. Oracle to PostgreSQL
    3. Oracle to Redshift
    4. SQL Server to Oracle
    5. SQL Server to PostgreSQL
    6. SQL Server to Redshift
    6. PostgreSQL to Oracle
    7. PostgreSQL to SQL Server
    8. PostgreSQL to Redshift
    9. Redshift to Oracle
    10. Redshift to SQL Server
    11. Redshift to PostgreSQL

The logical flow for accountability will be made availble below once the algorithm has been ratified.

## Logicals

### Purging

Creates 3 new tables : 

1. PURGE_REQUEST : Header level status posting for all scripts
2. PURGE_REQUEST_DETAILS : Details for each purge action
3. PURGE_MODULE_INPUT : Log level details of execution for each module

Single time execution functions within the resultant script : 

1. CREATE_MODULE_REQS : To be execute once for any one module depending on the same schema
2. DELETE_MODULE_REQS : May be executed for all modules depending on the same schema, deletes the 3 aforementioned tables

Entry point : 

1. RUN_PURGE : Runs the purge script for the specified logic.