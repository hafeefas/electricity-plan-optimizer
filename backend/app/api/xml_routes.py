from flask import Blueprint, jsonify
import os
import logging
from ..services.xml_service import validate_xml_structure, query_xml_data
from ..utils.config import XML_FILE_PATH

logger = logging.getLogger(__name__)
xml_bp = Blueprint('xml', __name__)

@xml_bp.route('/api/xml/validate')
def validate_xml():
    """Validate XML against schema"""
    is_valid, message = validate_xml_structure(XML_FILE_PATH)
    
    if is_valid:
        return jsonify({
            "status": "valid",
            "message": message
        })
    else:
        return jsonify({
            "status": "invalid",
            "message": message
        }), 400

@xml_bp.route('/api/xml/query')
def query_xml():
    """Query XML data using XPath"""
    try:
        if not os.path.exists(XML_FILE_PATH):
            return jsonify({"error": "XML file not found"}), 404

        results = query_xml_data(XML_FILE_PATH)
        if results is None:
            return jsonify({
                "status": "error",
                "message": "Failed to query XML data"
            }), 500

        return jsonify({
            "status": "success",
            "results": results
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500 