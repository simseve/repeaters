# Ham Radio Repeaters in Italy

This web app download the latest list of Ham Radio repeaters in Italy from www.ik2ane.it and displays it online for easier consultation.

# Installation

`sudo pip install -r requirements.txt`

# Launch

`export FLASK_APP=app`

`flask app.py`

# since I moved to uvicorn use this

`uvicorn app:app --reload`

# Docker deployment
`docker build -t repeaters .`

`docker-compose up -d`
