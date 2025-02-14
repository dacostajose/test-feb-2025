import json
from datetime import timedelta

# Load the JSON data
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


def parse_time(time_str):
    day_offset, time = time_str.split('.')
    hours, minutes = map(int, time.split(':'))
    return timedelta(days=int(day_offset), hours=hours, minutes=minutes)

def convert_timedelta_to_human_readable(td):
    total_hours = td.days * 24 + td.seconds // 3600
    minutes = (td.seconds % 3600) // 60
    final_hours = total_hours % 24
    return f"{final_hours:02}:{minutes:02}"

def generate_start_end_time_report(duties, vehicles):
    report = []
    for duty_id, duty_events in duties.items():
        start_times = []
        end_times = []
        for event in duty_events:
            vehicle_id = event.get('vehicle_id')
            vehicle_event_sequence = event.get('vehicle_event_sequence')
            if vehicle_id:
                vehicle_events = vehicles.get(vehicle_id).get('vehicle_events')
                v_event = {}
                if vehicle_events:
                    for e in vehicle_events:
                        if int(e.get('vehicle_event_sequence')) == vehicle_event_sequence:
                            v_event = e
                            break
                if v_event.get('vehicle_event_type') != 'service_trip':
                    start_times.append(parse_time(v_event.get('start_time')))
                    end_times.append(parse_time(v_event.get('end_time')))
                else:
                    trip_id = v_event.get('trip_id')
                    trip = trips.get(trip_id)
                    if trip:
                        start_times.append(parse_time(trip.get('departure_time')))
                        end_times.append(parse_time(trip.get('arrival_time')))

        start_time = convert_timedelta_to_human_readable(min(start_times))
        end_time = convert_timedelta_to_human_readable(max(end_times))
        report.append((duty_id, start_time, end_time))
    return report

start_end_time_report = generate_start_end_time_report(duties, vehicles)

for row in start_end_time_report:
    print(f"Duty ID: {row[0]}, Start Time: {row[1]}, End Time: {row[2]}")
