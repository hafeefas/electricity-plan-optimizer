from flask import Blueprint, jsonify, request
import os
import logging
import requests
from ..services.xml_service import process_xml_data
from ..utils.config import API_KEY, XML_FILE_PATH, DATA_DIR

logger = logging.getLogger(__name__)
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return "Student Energy Plan Optimizer is running inside Docker!"

@main_bp.route('/testxml', methods=['GET'])
@main_bp.route('/testxml/', methods=['GET'])
def test_xml():
    """Test endpoint to verify XML processing"""
    logger.info(f"Test XML endpoint was called. Method: {request.method}")
    logger.info(f"Request URL: {request.url}")
    logger.info(f"Request Headers: {dict(request.headers)}")
    
    try:
        logger.info(f"Looking for XML file at: {os.path.abspath(XML_FILE_PATH)}")
        
        if not os.path.exists(XML_FILE_PATH):
            logger.error("XML file not found")
            return jsonify({"error": "XML file not found. Please run /fetch-rates first"}), 404

        logger.info("XML file found, parsing...")
        try:
            from lxml import etree
            tree = etree.parse(XML_FILE_PATH)
            logger.info("XML parsing successful")
        except Exception as parse_error:
            logger.error(f"XML parsing error: {str(parse_error)}")
            return jsonify({"error": f"XML parsing error: {str(parse_error)}"}), 500
        
        logger.info("Running XPath queries...")
        try:
            test_results = {
                "basic_info": {
                    "total_rows": len(tree.xpath("//row")),
                    "years": tree.xpath("//row/period/text()")[:5],
                    "sectors": list(set(tree.xpath("//row/sectorName/text()"))),
                },
                "residential_data": {
                    "years": tree.xpath("//row[sectorid='RES']/period/text()"),
                    "descriptions": tree.xpath("//row[sectorid='RES']/stateDescription/text()")
                },
                "commercial_data": {
                    "years": tree.xpath("//row[sectorid='COM']/period/text()"),
                    "descriptions": tree.xpath("//row[sectorid='COM']/stateDescription/text()")
                },
                "recent_data": {
                    "latest_year": tree.xpath("//row/period/text()")[0],
                    "all_sectors_latest": tree.xpath("//row[period='2023']/sectorName/text()")
                }
            }
            logger.info("XPath queries completed successfully")
        except Exception as xpath_error:
            logger.error(f"XPath query error: {str(xpath_error)}")
            return jsonify({"error": f"XPath query error: {str(xpath_error)}"}), 500

        logger.info("Returning successful response")
        return jsonify({
            "status": "success",
            "message": "XML processing test results",
            "results": test_results
        })

    except Exception as e:
        logger.error(f"Unexpected error in test_xml: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@main_bp.route('/fetch-rates')
def fetch_rates():
    logger.info("fetch_rates endpoint was called")
    try:
        url = f"https://api.eia.gov/v2/electricity/retail-sales/data/?api_key={API_KEY}&frequency=annual&data=value&facets[stateid][]=NY&out=xml"

        response = requests.get(url)

        if response.status_code != 200:
            logger.error(f"Status code: {response.status_code}")
            logger.error(f"Response text: {response.text}")
            return f"Failed to fetch data from EIA API. Status code: {response.status_code}", 500

        os.makedirs(DATA_DIR, exist_ok=True)

        with open(XML_FILE_PATH, 'wb') as f:
            f.write(response.content)

        processed_data = process_xml_data(XML_FILE_PATH)
        
        return jsonify({
            "message": "Electricity rate data fetched and processed successfully",
            "data": processed_data
        })

    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        return f"An error occurred: {e}", 500 