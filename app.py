from flask import Flask, render_template, request, redirect
from create_db import import_list
import sqlite3
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

scheduler = BackgroundScheduler()
scheduler.add_job(func=import_list, trigger="interval", weeks=1)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

# @app.before_request
# def before_request():
#     if request.url.startswith('http://'):
#         url = request.url.replace('http://', 'https://', 1)
#         code = 301
#         return redirect(url, code=code)

@app.route('/')
def index():
    # Connecting to a template (html file)
    conn = sqlite3.connect('app.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM ponti')
    ponti = cur.fetchall()

    return render_template('index.html', ponti=ponti)

if __name__ == '__main__':
    app.run()