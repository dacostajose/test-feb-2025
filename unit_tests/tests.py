import unittest
import sys
import os
import json

from flask import Flask
from flask.testing import FlaskClient
from unittest.mock import patch, mock_open
from datetime import timedelta
from mock_data.data import sample_mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from report.classes import Report
from app import app

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        """Test setup for flask"""
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.report.generate_duty_reports')
    def test_generate_duty_reports(self, mock_generate_duty_reports):
        """Test the route /reports/duty_reports."""
        mock_generate_duty_reports.return_value = [
            {'Duty id': '1', 'Start time': '08:00', 'End time': '17:00'}
        ]
        response = self.app.get('/reports/duty_reports')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Duty id', response.json[0])

    @patch('app.report.generate_duty_reports')
    def test_generate_full_duty_reports(self, mock_generate_duty_reports):
        """Test the route /reports/full_duty_reports."""
        mock_generate_duty_reports.return_value = [
            {'Duty id': '1', 'Start time': '08:00', 'End time': '17:00', 'Start stop description': 'Stop A', 'End stop description': 'Stop B'}
        ]
        response = self.app.get('/reports/full_duty_reports')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Start stop description', response.json[0])

    @patch('app.report.generate_duty_breaks_report')
    def test_generate_duty_breaks_report(self, mock_generate_duty_breaks_report):
        """Test the route /reports/duty_breaks_report."""
        mock_generate_duty_breaks_report.return_value = [
            {'Duty id': '1', 'Start time': '08:00', 'End time': '17:00', 'Break start time': '12:00', 'Break duration': '30 min', 'Break stop name': 'Stop C'}
        ]
        response = self.app.get('/reports/duty_breaks_report')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Break start time', response.json[0])

    @patch('app.report.generate_duty_reports')
    @patch('utils.csv_utils.create_csv_based_on_arrays')
    def test_download_duty_reports(self, mock_create_csv, mock_generate_duty_reports):
        """Test the route /download/reports/duty_reports."""
        mock_generate_duty_reports.return_value = [
            {'Duty id': '1', 'Start time': '08:00', 'End time': '17:00'}
        ]
        mock_create_csv.return_value = "Duty id,Start time,End time\n1,08:00,17:00"
        response = self.app.get('/download/reports/duty_reports')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'text/csv')
        self.assertIn('attachment;filename=duty_report.csv', response.headers['Content-Disposition'])

    @patch('app.report.generate_duty_reports')
    @patch('utils.csv_utils.create_csv_based_on_arrays')
    def test_download_full_duty_reports(self, mock_create_csv, mock_generate_duty_reports):
        """Test the route /download/reports/full_duty_reports."""
        mock_generate_duty_reports.return_value = [
            {'Duty id': '1', 'Start time': '08:00', 'End time': '17:00', 'Start stop description': 'Stop A', 'End stop description': 'Stop B'}
        ]
        mock_create_csv.return_value = "Duty id,Start time,End time,Start stop description,End stop description\n1,08:00,17:00,Stop A,Stop B"
        response = self.app.get('/download/reports/full_duty_reports')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'text/csv')
        self.assertIn('attachment;filename=full_duty_reports.csv', response.headers['Content-Disposition'])

    @patch('app.report.generate_duty_breaks_report')
    @patch('utils.csv_utils.create_csv_based_on_arrays')
    def test_download_duty_breaks_report(self, mock_create_csv, mock_generate_duty_breaks_report):
        """Test the route /download/reports/duty_breaks_report."""
        mock_generate_duty_breaks_report.return_value = [
            {'Duty id': '1', 'Start time': '08:00', 'End time': '17:00', 'Break start time': '12:00', 'Break duration': '30 min', 'Break stop name': 'Stop C'}
        ]
        mock_create_csv.return_value = "Duty id,Start time,End time,Break start time,Break duration,Break stop name\n1,08:00,17:00,12:00,30 min,Stop C"
        response = self.app.get('/download/reports/duty_breaks_report')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'text/csv')
        self.assertIn('attachment;filename=break_reports.csv', response.headers['Content-Disposition'])


class TestReport(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps(sample_mock))
    def test_generate_duty_reports(self, mock_file):
        report = Report('dummy_path')
        result = report.generate_duty_reports()
        expected = [
            ['1', '07:00', '09:00']
        ]
        self.assertEqual(result, expected)

    def test_parse_time(self):
        result = Report.parse_time("1.15:30")
        expected = timedelta(days=1, hours=15, minutes=30)
        self.assertEqual(result, expected)

    def test_convert_timedelta_to_human_readable(self):
        """Testa o método convert_timedelta_to_human_readable."""
        td = timedelta(days=1, hours=15, minutes=30)
        result = Report.convert_timedelta_to_human_readable(td)
        expected = "15:30"
        self.assertEqual(result, expected)

    def test_calc_time_difference_in_minutes(self):
        """Testa o método calc_time_difference_in_minutes."""
        start_time = timedelta(hours=8)
        end_time = timedelta(hours=10)
        result = Report.calc_time_difference_in_minutes(start_time, end_time)
        expected = 120
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
