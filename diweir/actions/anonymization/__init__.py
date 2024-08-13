
import logging
import os
from diweir.config import AnonymizationConfiguration
from diweir.utils import get_app_location

app_data_dir = get_app_location()

logger = logging.getLogger("task_engine")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s")
log_loc = os.path.join(app_data_dir, 'logs')
log_file = os.path.join(log_loc, 'task_execution.log')
if not os.path.exists(log_loc) and not os.path.isfile(log_loc):
    os.makedirs(log_loc)
    if os.path.isfile(log_file):
        open(log_file, "w").close()

file_handler = logging.FileHandler(log_file, mode="a", encoding=None, delay=False)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.info(f"Logging to {log_file}")

def anonymize(config : AnonymizationConfiguration):
    pass