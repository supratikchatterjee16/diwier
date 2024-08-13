import random

# PiiType definitions
anonymization_map = {
    'empty' : {'desc' : 'Insert a NULL value', 'op' : lambda : None},
    'integer' : {'desc' : 'Insert an integer', 'op' : lambda a=10, b=0 : int(random.random() * 10 ** a) if b == 0 else round(random.random() * 10 ** a, b)},
    # 'string' : {'desc' : 'Insert a string', 'op' : lambda : None},
    'name' : {'desc' : 'Prepared full name', 'op' : lambda : None},
    'first-name' : {'desc' : 'First name', 'op' : lambda : None},
    'last-name' : {'desc' : 'Last name', 'op' : lambda : None},
    'isd' : {'desc' : 'International Dialing code', 'op' : lambda : None},
    'phone' : {'desc' : 'Phone Number', 'op' : lambda : None},
    'national-id' : {'desc' : 'National Identifier', 'op' : lambda : None},
    'card' : {'desc' : 'Credit/Debit Card Number', 'op' : lambda : None},
    'address' : {'desc' : 'Address', 'op' : lambda : None},
    'building' : {'desc' : 'Building Number', 'op' : lambda : None},
    'street' : {'desc' : 'Street', 'op' : lambda : None},
    'city' : {'desc' : 'City', 'op' : lambda : None},
    'province' : {'desc' : 'Province/State/Region', 'op' : lambda : None},
    'country' : {'desc' : 'Country', 'op' : lambda : None},
    'pin' : {'desc' : 'Area PIN code', 'op' : lambda : None},
    'dob' : {'desc' :'Date of Birth', 'op' : lambda : None}
}

# The following is for auto configuration of mocking data
# age, sex, income level, race, employment, location, homeownership, and level of education
demographics_config_allowed = {
    'location' : [],
    'age' : [],
    'income-level' : [],
    'race' : [], 
    'employment' : [],
    'homeownership' : [],
    'education-level' : []
}

# Databases supported

db_providers = [
    {'provider' : 'oracle+cx_oracle', 'name' : 'Oracle'},
    {'provider' : 'postgresql+psycopg2', 'name' : 'PostgreSQL'},
    {'provider' : 'mysql+mysqldb', 'name' : 'MySQL'},
    {'provider' : 'mssql+pyodbc', 'name' : 'MS SQL Server'},
    {'provider' : 'mssql+pymssql', 'name' : 'MS SQL Server'},
    {'provider' : 'sqlite', 'name' : 'SQLite'},
    {'provider' : 'redshift+psycopg2', 'name' : 'Amazon Redshift'},
    {'provider' : 'cockroachdb', 'name' : 'CockroachDB'},
    {'provider' : 'db2+ibm_db', 'name' : 'IBM DB2'},
]

envs = [
    {'name' : 'Dev', 'desc' : 'Development environment'},
    {'name' : 'Sandbox', 'desc' : 'Production-like environment for experimentation'},
    {'name' : 'Test', 'desc' : 'Testing environment for development environment(also central development env)'},
    {'name' : 'UAT', 'desc' : 'User Acceptance Testing. Used by Business Analysts and Product Managers'},
    {'name' : 'FT', 'desc' : 'Functional Testing. Used by BAs and testers for functional tests.'},
    {'name' : 'QA', 'desc' : 'Quality Assurance. Used by software testers and product managers.'},
    {'name' : 'PT', 'desc' : 'Performance Testing. Used by engineers for stress testing softwares.'},
    {'name' : 'STG', 'desc' : 'Staging. Stage your software for validation prior to production deployment. Used by POs and DevOps/Ops.'},
    {'name' : 'Pre-PROD', 'desc' : 'Pre-Production environment for alpha testing.'},
    {'name' : 'PROD', 'desc' : 'Production environment.'}
]

roles = [
    {'name' : 'app-admin', 'description' : ''},
    {'name' : 'data-architect', 'description' : ''},
    {'name' : 'business-analyst', 'description' : ''},
    {'name' : 'db-admin', 'description' : ''},
    {'name' : 'enterprise-architect', 'description' : ''},
]