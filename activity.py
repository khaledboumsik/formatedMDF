from flask import Flask, request, jsonify
from Front.Healpers.CSVLoader import process_csv_files
import subprocess
import os

app = Flask(__name__)

@app.route('/generate-report', methods=['POST'])
def generate_report():
    # Get the JSON data from the request
    data = request.get_json()

    # Extract the configuration file path
    config_file_path = data.get('config_file_path')

    if not config_file_path:
        return jsonify({"error": "Configuration file path is required"}), 400

    # Process the CSV files
    try:
        csv_path = process_csv_files(config_file_path)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Generate the report
    try:
        Warning("file is stored in ",csv_path)
        
        command = ['python', os.path.join('front', 'SubWidgets', 'table.py'), csv_path]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            return jsonify({"error": stderr}), 500

        return jsonify({"message": "Report generated successfully", "stdout": stdout}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
