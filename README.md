# DI-WEIR

A tool for DataOps on a RDBMS systems.
The utility is aims to help with :

1. Purging(with/without archival)
2. Backup(with Anonymzation)
3. Modelling(OLTP & OLAP)
4. Anonymization
5. Test data configuration
6. RDBMS migration
7. NoSQL migration(MongoDB)

It also provides the following :

1. Monitoring(role based)
    - storage health
    - Average connections and usage
    - Program executions
    - Authorizations
2. Authentication & authorization tracking.

**Note : This is in development and the above lists the target features. Check relases for feature releases.**

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

Use the following command to find all details related to it's execution : 

```shell
diwier -h
```

## API

This can be utilized in various ways, but using this is required only in the scenario a custom solution is required.

## Status

This is a Work in Progress(WIP). As a lot of details are required to go into it, this will take some time and effort to complete.

## Contributing

Please do contribute to this however possible. We aim to provide data handling solutions to fast track data management efforts, while providing a solution that allows for full accountability during execution.

Done : 

To-do :

1. Purging with backup
    1. PostgreSQL
    2. Redshift
    3. SQL Server
    4. Oracle
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
