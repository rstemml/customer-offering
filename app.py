#!/usr/bin/env python3
"""
Customer Offering Generator - Web UI

Philosophy: Beauty and simplicity in every interaction.
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import yaml
import json
import sys
import traceback
from pathlib import Path
from datetime import date
import tempfile
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.models import Offer
from src.generator import generate_offer
from src.calculator import PriceCalculator
from src.extractor import ChatExtractor

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = Path(tempfile.gettempdir()) / 'customer-offering-uploads'
UPLOAD_FOLDER.mkdir(exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/extract', methods=['POST'])
def extract_from_text():
    """Extract offer data from natural language text"""
    try:
        data = request.get_json()
        text = data.get('text', '')

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        # Extract data
        extractor = ChatExtractor()
        extracted_data = extractor.extract_from_text(text)

        return jsonify({
            'success': True,
            'data': extracted_data,
            'yaml': extractor.to_yaml()
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/validate', methods=['POST'])
def validate_offer():
    """Validate offer data"""
    try:
        data = request.get_json()

        # Try to create Offer model (validates data)
        offer = Offer(**data)

        # Calculate pricing
        calculator = PriceCalculator(offer)
        breakdown = calculator.calculate_breakdown()

        return jsonify({
            'success': True,
            'valid': True,
            'pricing': {
                'subtotal': float(breakdown.subtotal),
                'discount_percent': float(breakdown.discount_percent),
                'discount_amount': float(breakdown.discount_amount),
                'subtotal_after_discount': float(breakdown.subtotal_after_discount),
                'tax_percent': float(breakdown.tax_percent),
                'tax_amount': float(breakdown.tax_amount),
                'total': float(breakdown.total),
                'total_formatted': breakdown.format_currency(breakdown.total)
            },
            'team_size': calculator.get_team_size(),
            'team_costs': [tc.to_dict() for tc in breakdown.team_costs]
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'success': False,
            'valid': False,
            'error': str(e)
        }), 400


@app.route('/api/generate', methods=['POST'])
def generate_offer_api():
    """Generate PowerPoint offer"""
    try:
        data = request.get_json()

        # Validate and create offer
        offer = Offer(**data)

        # Generate filename
        customer_slug = offer.customer.name.lower().replace(' ', '-').replace('/', '-')
        timestamp = date.today().isoformat()
        filename = f"{customer_slug}-offer-{timestamp}.pptx"

        # Output path
        output_path = UPLOAD_FOLDER / filename

        # Generate offer
        template_path = "templates/offer_template.pptx"
        generate_offer(offer, template_path, str(output_path))

        return jsonify({
            'success': True,
            'filename': filename,
            'download_url': f'/api/download/{filename}'
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/<filename>')
def download_file(filename):
    """Download generated PowerPoint file"""
    try:
        file_path = UPLOAD_FOLDER / filename

        if not file_path.exists():
            return jsonify({'error': 'File not found'}), 404

        return send_file(
            file_path,
            mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload and parse YAML/JSON file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Read file content
        content = file.read().decode('utf-8')

        # Parse based on extension
        if file.filename.endswith('.json'):
            data = json.loads(content)
        elif file.filename.endswith('.yaml') or file.filename.endswith('.yml'):
            data = yaml.safe_load(content)
        else:
            return jsonify({'error': 'Unsupported file type. Use YAML or JSON'}), 400

        # Validate
        offer = Offer(**data)

        return jsonify({
            'success': True,
            'data': data,
            'yaml': yaml.dump(data, default_flow_style=False, allow_unicode=True)
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'version': '0.1.0'})


if __name__ == '__main__':
    print("🎨 Customer Offering Generator - Web UI")
    print("=" * 50)
    print("Starting server...")
    print("\n🌍 Open in browser: http://localhost:5000")
    print("\nPress Ctrl+C to stop\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
