from flask import Flask, request, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import os
import json
import logging
from cvetomap.cvetomap import map

app = Flask(__name__)
socketio = SocketIO(app)

# Directory to save the download files
DOWNLOAD_DIR = os.path.join(app.root_path, 'static', 'downloads')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

@socketio.on('analyze_cve')
def handle_analyze_cve(data):
    cve_id = data['cve_id']
    logging.info(f"Received CVE ID: {cve_id}")

    # Validate CVE ID format
    if not cve_id.startswith("CVE-"):
        error_message = "Invalid CVE ID format. Please use the format 'CVE-YYYY-NNNNN'."
        logging.error(f"Invalid CVE ID format: {cve_id}")
        emit('error', {'message': error_message})
        return

    try:
        emit('progress', {'percentage': 10, 'message': 'Initializing analysis...'})

        # Call the main function
        technical_analysis, executive_analysis, mitre_layer, stix_obj = map.main(
            cve_id,
            "33be7796-4783-41fe-983f-09672b60cd16",
            "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",
            "nvd"
        )
        emit('progress', {'percentage': 50, 'message': 'Processing analysis...'})

        # File paths
        files = {
            'technical_analysis': f"{cve_id}_Technical_Analysis.md",
            'executive_analysis': f"{cve_id}_Executive_Analysis.md",
            'mitre_layer': f"{cve_id}_MITRE_ATT&CK_Layer.json",
            'stix_obj': f"{cve_id}_STIX_Bundle.json"
        }

        # Save files
        with open(os.path.join(DOWNLOAD_DIR, files['technical_analysis']), 'w') as f:
            f.write(technical_analysis)
        with open(os.path.join(DOWNLOAD_DIR, files['executive_analysis']), 'w') as f:
            f.write(executive_analysis)
        with open(os.path.join(DOWNLOAD_DIR, files['mitre_layer']), 'w') as f:
            f.write(json.dumps(mitre_layer, indent=4))
        with open(os.path.join(DOWNLOAD_DIR, files['stix_obj']), 'w') as f:
            f.write(json.dumps(stix_obj, indent=4))

        logging.info(f"Files saved for {cve_id}")
        emit('progress', {'percentage': 90, 'message': 'Reports Generated Successfully!'})

        emit('complete', {'cve_id': cve_id, 'files': files})

    except Exception as e:
        logging.error(f"Error processing CVE ID {cve_id}: {e}")
        emit('error', {'message': str(e)})

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    socketio.run(app, debug=True)