# Repeater's Data Importer API

This FastAPI application, named 'Repeaters', is designed to import and serve repeater data from a specified source. It uses a SQLite database to store the imported data and provides endpoints to access this data.

## Features

- **Data Import**: Automatically imports repeater data from a specified URL and stores it in a SQLite database.
- **API Endpoint**: A secured endpoint to fetch the latest imported data.
- **Web Interface**: An HTML interface to view the data.
- **Scheduled Imports**: Uses APScheduler to schedule weekly data imports.
- **Logging**: Detailed logging of application activities and API requests.

## Installation

To set up and run the application, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone [repository-url]
   cd [repository-directory]
   ```

2. **Set Up Environment**:
   - It's recommended to use a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
     ```
   - Install the required packages:
     ```bash
     pip install -r requirements.txt
     ```

3. **Environment Variables**:
   - Set the `API_KEY` environment variable for secured API access.

4. **Run the Application**:
   ```bash
   uvicorn main:app --reload
   ```

## Usage

- **Access the Web Interface**: Open your browser and navigate to `http://localhost:8000`.
- **Fetch Data via API**: Send a GET request to `http://localhost:8000/data` with the header `x-api-key: YOUR_API_KEY`.

# Ham Radio Repeaters in Italy

This web app download the latest list of Ham Radio repeaters in Italy from www.ik2ane.it and displays it online for easier consultation.

### Installation

`sudo pip install -r requirements.txt`

### Launch

`export FLASK_APP=app`

`flask app.py`

### since I moved to uvicorn use this

`uvicorn app:app --reload`

#### Docker deployment
`docker build -t repeaters .`

`docker-compose up -d`


## API Endpoints

- `GET /`: The home page showing the latest data.
- `GET /data`: Returns the latest imported data in JSON format.

## Scheduled Data Import

The application is configured to automatically import new data every week. The import time and status are logged.

## Logging

Logs are written to `[APP_NAME].log`. Each session has a unique session ID for easier tracking and debugging.

## License

[Specify License Here]

## Contact

[Your Contact Information]
```

Feel free to customize the `README.md` file to include any additional information, instructions, or contact details specific to your project.
