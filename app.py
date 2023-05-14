import logging
import os
import uuid
from fastapi import FastAPI, Depends, HTTPException, status, Header, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import datetime
import pandas as pd
from typing import List, Optional
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

from fastapi.middleware.cors import CORSMiddleware

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
DATA_URL = 'http://www.ik2ane.it/pontixls.xls'
API_KEY = '643cd615b54b64e48a3fb8545de2d44c379d9798ba86e08c7b5559519dc050f3'
TRUSTED_DOMAIN = '4cae.l.time4vps.cloud'
APP_NAME='repeaters'

engine = create_engine(
    DATABASE_URL, echo=False, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["TRUSTED_DOMAIN"],  # Allows all origins change to TRUSTED DOMAIN
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

scheduler = BackgroundScheduler()
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

# Configure logging
logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s %(name)s %(levelname)s: %(message)s")
file_logging = logging.FileHandler(f"{APP_NAME}.log")
file_logging.setFormatter(formatter)
logger.addHandler(file_logging)

# Generate a unique session ID for each session
session_id = str(uuid.uuid4())
logger.info(f"[Session ID: {session_id}] created")

# Additional property to store the last import time
last_import = None

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_token_header(x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_KEY:
        logger.warning("Invalid API Key: %s", x_api_key)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid API Key"
        )
    return x_api_key

def create_sqlite_db_if_not_exists():
    if not database_exists(engine.url):
        create_database(engine.url)
        logger.info("Created database %s", engine.url)

@app.on_event("startup")
async def startup_event():
    create_sqlite_db_if_not_exists()
    import_list()
    logger.info(f"[Session ID: {session_id}] First import succedded")

@scheduler.scheduled_job('interval', weeks=1)
def import_list():
    global last_import
    logger.info(f"[Session ID: {session_id}] Importing data...")
    with engine.begin() as conn:
        url = DATA_URL
        df = pd.read_excel(url)
        df = df.dropna(subset=['(F)req'])
        df = df.drop(['Agg.', '(K)m', 'Gradi', '(O)rdkey', 'JN45OL'], axis=1)
        df.dropna(subset=['(N)ome'], inplace=True)

        # Write to SQL
        df.to_sql('ponti', con=conn, if_exists='replace')

    last_import = datetime.datetime.now()

@app.get("/data", dependencies=[Depends(get_token_header)])
def get_data(db: Session = Depends(get_db)):
    result = db.execute(text('SELECT * FROM ponti'))
    rows = result.fetchall()
    data = []
    for row in rows:
        row_dict = dict(zip(result.keys(), row))
        data.append(row_dict)
    logger.info(f"[Session ID: {session_id}] Data requested")
    return {"data": data, "last_import": last_import}

@app.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    logger.info(f"[Session ID: {session_id}] Index requested")
    result = db.execute(text('SELECT * FROM ponti'))
    rows = result.fetchall()
    return templates.TemplateResponse("index.html", {"request": request, "ponti": rows, "update": last_import})



# Log the startup message
logger.info(f"[Session ID: {session_id}] Starting the application...")

