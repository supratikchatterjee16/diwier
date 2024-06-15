from contextlib import asynccontextmanager
from diweir.config import ServerConfiguration
from fastapi import FastAPI
from sqlalchemy import Engine
import uvicorn

import diweir.models as orm

rest_app = FastAPI()
rest_config : ServerConfiguration | None = None
engine : Engine | None = None

@asynccontextmanager
async def lifespan(app : FastAPI):
    yield

# API Endpoints
# GET / : Provide Frontend
# GET /data?params=? : Get information stored in a table, query based on allowed column names.
# POST /anonymize : Send anonymization data to be created
# UPDATE /anonymize : Send anonymization data to be updated
# DELETE /anonymize : Remove anonymization data
# POST /archive : Send archival information data to be created
# PUT /archive : Send archival information data to be created
# DELETE /archive : Delete archival information
# POST /purge : Send purge information data to be created
# PUT /purge : Send purge information data to be created
# DELETE /purge : Delete purge information
# POST /migrate : Send migration information data to be created
# PUT /migrate : Send migration information data to be created
# DELETE /migrate : Delete migration information


@rest_app.get('/')
async def root():
    return 'Hello'

@rest_app.get('/health')
async def health_check():
    '''
    Endpoint for health checks. Checks for the following :
    
    1. Memory
    2. Node CPU utilization
    ''' 
    return {'status' : 'ok'}

@rest_app.get('/data')
async def fetch_data():
    return {"table" : "something", "data" : []}

def start_server(config : ServerConfiguration):
    orm.create_all(config.get_conn().engine)
    uvicorn.run(rest_app, host = config.host, port=config.port)
