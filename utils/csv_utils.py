import csv
from io import StringIO

def create_csv_based_on_arrays(data, headers):
    """Creates a CSV file based on the data and headers provided."""
    output = StringIO()
    csv_writer = csv.writer(output)
    csv_writer.writerow(headers)
    for row in data:
        csv_writer.writerow(row)
    csv_content = output.getvalue()
    output.close()
    return csv_content