# Flask API for Duty Reports

This project is a Flask API that generates duty reports and allows downloading these reports in CSV format. The API is structured to be modular and efficient, using different modules to generate reports and handle CSV data.

## Table of Contents

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Project Structure](#project-structure)
4. [Running the Application](#running-the-application)
5. [Using the API](#using-the-api)
6. [Unit Tests](#unit-tests)

## Requirements

- Python 3.10.0
- Flask

## Installation

### Set Up a Virtual Environment

It's recommended to create a virtual environment to isolate project dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Install Dependencies

Install the dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Project Structure

- **`app.py`**: The main file that sets up and runs the Flask application.
- **`utils/csv_utils.py`**: Utility module for CSV-related functions.
- **`report/classes.py`**: Module containing the logic to generate different types of reports.
- **`base_script/`**: Directory containing the basic version of the code.
- **`unit_tests/`**: Directory containing the unit tests.

## Running the Application

To start the Flask application, run the following command in the terminal:

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5500/`.

## Using the API

### Report Generation Endpoints

- **Generate Duty Report**:
  - **URL**: `/reports/duty_reports`
  - **Method**: GET
  - **Description**: Returns a duty report in JSON format.

- **Generate Full Duty Report**:
  - **URL**: `/reports/full_duty_reports`
  - **Method**: GET
  - **Description**: Returns a full duty report, including trip information, in JSON format.

- **Generate Duty Breaks Report**:
  - **URL**: `/reports/duty_breaks_report`
  - **Method**: GET
  - **Description**: Returns a duty breaks report in JSON format.

### CSV Download Endpoints

- **Download Duty Report**:
  - **URL**: `/download/reports/duty_reports`
  - **Method**: GET
  - **Description**: Downloads the duty report in CSV format.

- **Download Full Duty Report**:
  - **URL**: `/download/reports/full_duty_reports`
  - **Method**: GET
  - **Description**: Downloads the full duty report in CSV format.

- **Download Duty Breaks Report**:
  - **URL**: `/download/reports/duty_breaks_report`
  - **Method**: GET
  - **Description**: Downloads the duty breaks report in CSV format.

## Unit Tests

To run the unit tests, execute the following command:

```bash
python unit_tests/tests.py
```
