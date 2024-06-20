import os
import uvicorn
from sqlalchemy import Engine
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from contextlib import asynccontextmanager

import diweir.models as orm
from diweir.config import ServerConfiguration

rest_app = FastAPI()
rest_config : ServerConfiguration | None = None
engine : Engine | None = None

frontend_path = os.path.join(Path(__file__).parent.parent, 'res', 'front', 'out')
print(frontend_path, Path(frontend_path).is_dir())
rest_app.mount("/", StaticFiles(directory=frontend_path, html = True), name="frontend")

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


# @rest_app.get('/')
# async def root():
#     return 'Hello'

@rest_app.get('/api/health')
async def health_check():
    '''
    Endpoint for health checks. Checks for the following :
    
    1. Memory
    2. Node CPU utilization
    ''' 
    return {'status' : 'ok'}

@rest_app.get('/api/data')
async def fetch_data():
    return {"table" : "something", "data" : []}

def start_server(config : ServerConfiguration):
    orm.create_all(config.get_conn().engine)
    uvicorn.run(rest_app, host = config.host, port=config.port)
