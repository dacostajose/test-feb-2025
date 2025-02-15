import json

class Report:
    def __init__(self, file_path):
        with open('file/mini_json_dataset.json') as f:
            data = json.load(f)

        stops = {}
        trips = {}
        vehicles = {}
        duties = {}

        # Extract relevant data
        for stop in data['stops']:
            stop_id = stop.get('stop_id')
            stops[stop_id] = stop

        for trip in data['trips']:
            trip_id = trip.get('trip_id')
            trips[trip_id] = trip

        for vehicle in data['vehicles']:
            vehicle_id = vehicle.get('vehicle_id')
            vehicles[vehicle_id] = vehicle

        for duty in data['duties']:
            duty_id = duty.get('duty_id')
            duties[duty_id] = duty.get('duty_events')

