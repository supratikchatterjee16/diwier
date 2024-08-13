import os
import appdirs
from pathlib import Path
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker

def get_app_location():
    app_name = 'diweir'
    app_author="conceivilize"
    return appdirs.user_data_dir(app_name, app_author)

def get_image():
    global image_blob
    if image_blob == None:
        path = Path(__file__)
        with open(os.path.join(path.parent.parent.absolute(), 'resources', 'no-image.png'), 'rb') as image_file:
            image_blob = image_file.read()
    return image_blob

@contextmanager
def session_scope(conn):
    session_local = sessionmaker()
    session= session_local()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
