from flask import Flask, jsonify, Response

from report.classes import Report
from utils.csv_utils import create_csv_based_on_arrays

app = Flask(__name__)

report = Report('file/mini_json_dataset.json')

@app.route('/reports/duty_reports', methods=['GET'])
def generate_duty_reports():
    return jsonify(report.generate_duty_reports())

@app.route('/reports/full_duty_reports', methods=['GET'])
def generate_full_duty_reports():
    return jsonify(report.generate_duty_reports(include_trip=True))

@app.route('/reports/duty_breaks_report', methods=['GET'])
def generate_duty_breaks_report():
    return jsonify(report.generate_duty_breaks_report())


@app.route('/download/reports/duty_reports', methods=['GET'])
def download_duty_reports():
    try:
        data = report.generate_duty_reports()
        headers = [
            'Duty id',
            'Start time',
            'End time'
        ]
        csv_content = create_csv_based_on_arrays(data, headers)

        return Response(
            csv_content,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=duty_report.csv"}
        )

    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/download/reports/full_duty_reports', methods=['GET'])
def download_full_duty_reports():
    try:
        data = report.generate_duty_reports(include_trip=True)
        headers = [
            'Duty id',
            'Start time',
            'End time',
            'Start stop description',
            'End stop description'
        ]
        csv_content = create_csv_based_on_arrays(data, headers)

        return Response(
            csv_content,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=full_duty_reports.csv"}
        )

    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/download/reports/duty_breaks_report', methods=['GET'])
def download_duty_breaks_report():
    try:
        data = report.generate_duty_breaks_report()
        headers = [
            'Duty id',
            'Start time',
            'End time',
            'Start stop description',
            'End stop description',
            'Break start time',
            'Break duration',
            'Break stop name'
        ]
        csv_content = create_csv_based_on_arrays(data, headers)

        return Response(
            csv_content,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=break_reports.csv"}
        )

    except Exception as e:
        return jsonify(error=str(e)), 500


if __name__ == '__main__':
    app.run(port=5500, debug=True)