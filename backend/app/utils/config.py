import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_KEY = os.getenv('EIA_API_KEY')

# API Sources
SOURCES = {
    'EIA': 'https://api.eia.gov/v2/electricity/retail-sales/data/',
    'NREL': 'https://developer.nrel.gov/api/utility-rates/v3.json',
    'DOE': 'https://api.energy.gov/data/'
}

# File paths
DATA_DIR = 'data'
XML_FILE_PATH = 'data/eia_retail_sales_ny.xml' 