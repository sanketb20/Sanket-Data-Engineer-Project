\# A5 - REST API Ingestion Pipeline



\## Project Overview



This project demonstrates a Python-based REST API ingestion pipeline.



The pipeline retrieves weather information for multiple cities from the OpenWeather API, stores the raw API responses as JSON files, consolidates the data into a CSV file, validates the consolidated dataset, and maintains a checkpoint for successful ingestion.



\## Technologies Used



\- Python 3.11

\- REST API

\- OpenWeather API

\- Requests

\- Pandas

\- python-dotenv

\- Pytest

\- PowerShell

\- Git and GitHub



\## Project Structure



```text

A5-REST-API-Ingestion/

│

├── config/

│   └── cities.txt

│

├── data/

│   ├── weather\_\*.json

│   └── weather\_all\_cities.csv

│

├── src/

│   ├── api\_client.py

│   ├── checkpoint.py

│   ├── consolidate\_weather.py

│   ├── main.py

│   ├── multi\_city\_ingestion.py

│   ├── transform.py

│   └── validate\_weather.py

│

├── state/

│   └── weather\_checkpoint.json

│

├── tests/

│   └── test\_a5\_pipeline.py

│

├── .env.example

├── .gitignore

├── cron\_scheduling.md

├── README.md

└── requirements.txt

