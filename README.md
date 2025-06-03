# Energy Data ETL Pipeline

A Flask-based ETL pipeline for processing energy data from EIA (Energy Information Administration) in XML format.

## Features
- XML data processing and validation
- RESTful API endpoints
- Docker containerization
- Data transformation and querying

## Setup
1. Clone the repository
2. Set up environment variables:
   ```
   EIA_API_KEY=your_api_key
   ```
3. Run with Docker:
   ```bash
   docker-compose up --build
   ```

## API Endpoints
- `/testxml/` - Test XML processing
- `/fetch-rates` - Fetch energy rates
- `/api/xml/validate` - Validate XML structure
- `/api/xml/query` - Query XML data

## Tech Stack
- Python 3.9
- Flask
- lxml/xmltodict
- Docker
- MySQL 