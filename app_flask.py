from flask import Flask, render_template
import sqlite3
import atexit
from flask_apscheduler import APScheduler
import datetime
import pandas as pd
from sqlalchemy import create_engine
import datetime

app = Flask(__name__)

last_import = datetime.datetime.now()

scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())



@scheduler.task('interval', id='import_1', weeks=1)
def import_list():

    global last_import 

    engine = create_engine('sqlite:///app.db', echo=False)

    url = 'http://www.ik2ane.it/pontixls.xls'
    df = pd.read_excel(url)
    df = df.dropna(subset=['(F)req'])
    df = df.drop(['Agg.', '(K)m', 'Gradi', '(O)rdkey', 'JN45OL'], axis=1)
    df.dropna(subset=['(N)ome'], inplace=True)

    # Write to SQL
    df.to_sql('ponti', con=engine, if_exists='replace')

    # Update the time of import as a global variable
    last_import = datetime.datetime.now()


@app.route('/')
def index():

    # DB operation: read all records
    conn = sqlite3.connect('app.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM ponti')
    ponti = cur.fetchall()
    
    return render_template('index.html', ponti=ponti, update=last_import)



if __name__ == '__main__':
    app.run()
