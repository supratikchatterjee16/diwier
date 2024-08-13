import logging
import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse

import diweir.dao as orm
from diweir.dao.common import *
from diweir.dao.anonymization import *
from diweir.config import ServerConfiguration

rest_app = FastAPI()
rest_config: ServerConfiguration | None = None

frontend_path = os.path.join(Path(__file__).parent.parent, "res", "front")

# Logging details
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter(
    "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s"
)
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)


@asynccontextmanager
async def lifespan(app: FastAPI):
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


@rest_app.get("/api/health")
async def health_check():
    """
    Endpoint for health checks. Checks for the following :

    1. Memory
    2. Node CPU utilization
    """
    return {"status": "UP"}


@rest_app.get("/api/data")
async def fetch_data():
    return {"table": "something", "data": []}


@rest_app.get("/api/database")
async def fetch_db_info():
    pass


@rest_app.post("/api/database")
async def add_database():
    pass


@rest_app.delete("/api/database")
async def delete_database():
    pass


# Frontend Routes
@rest_app.get("/")
async def serve_index():
    return FileResponse(os.path.join(frontend_path, "index.html"))


@rest_app.get("/{file_path:path}")
async def serve_files(file_path: str):
    logger.error(file_path)
    if "." not in file_path.split("/")[-1]:
        file_path += ".html"
    return FileResponse(os.path.join(frontend_path, file_path))


def start_server(config: ServerConfiguration):
    global rest_config
    rest_config = config
    # orm.create_all(config.get_conn().engine)
    conn = rest_config.get_conn()
    orm.Base.metadata.create_all(bind=conn.engine)
    orm.initialize(conn)
    uvicorn.run(rest_app, host=rest_config.host, port=rest_config.port)
