import os
from lxml import etree
import xmltodict
import logging

logger = logging.getLogger(__name__)

def process_xml_data(xml_file_path):
    """Process XML data using lxml"""
    try:
        # Parse XML file into a tree structure
        tree = etree.parse(xml_file_path)
        root = tree.getroot()

        # Convert XML to Python dictionary for easier processing
        xml_dict = xmltodict.parse(etree.tostring(root))

        # Extract and structure relevant data
        processed_data = {
            "timestamp": xml_dict.get("response", {}).get("timestamp"),
            "data": xml_dict.get("response", {}).get("data", []),
            "metadata": {
                "source": "EIA API",
                "format": "XML",
                "state": "NY"
            }
        }

        return processed_data

    except Exception as e:
        logger.error(f"Error processing XML: {e}")
        return None

def validate_xml_structure(xml_file_path):
    """Validate XML structure"""
    try:
        if not os.path.exists(xml_file_path):
            return False, "XML file not found"

        tree = etree.parse(xml_file_path)
        root = tree.getroot()

        if root is not None:
            return True, "XML is well-formed"
        else:
            return False, "XML is not well-formed"

    except Exception as e:
        return False, str(e)

def query_xml_data(xml_file_path):
    """Query XML data using XPath"""
    try:
        tree = etree.parse(xml_file_path)
        
        results = {
            "all_data_points": tree.xpath("//data/value"),
            "years": tree.xpath("//data/period"),
            "values": tree.xpath("//data/value/text()")
        }

        return results

    except Exception as e:
        logger.error(f"Error querying XML: {e}")
        return None 