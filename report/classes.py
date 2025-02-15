import json
from datetime import timedelta

class Report:
    def __init__(self, file_path):
        with open(file_path) as f:
            data = json.load(f)

        self.stops = {}
        self.trips = {}
        self.vehicles = {}
        self.duties = {}

        # Extract relevant data
        for stop in data['stops']:
            stop_id = stop.get('stop_id')
            self.stops[stop_id] = stop

        for trip in data['trips']:
            trip_id = trip.get('trip_id')
            self.trips[trip_id] = trip

        for vehicle in data['vehicles']:
            vehicle_id = vehicle.get('vehicle_id')
            self.vehicles[vehicle_id] = vehicle

        for duty in data['duties']:
            duty_id = duty.get('duty_id')
            self.duties[duty_id] = duty.get('duty_events')
    
    @staticmethod
    def parse_time(time_str):
        day_offset, time = time_str.split('.')
        hours, minutes = map(int, time.split(':'))
        return timedelta(days=int(day_offset), hours=hours, minutes=minutes)
    
    @staticmethod
    def convert_timedelta_to_human_readable(td):
        total_hours = td.days * 24 + td.seconds // 3600
        minutes = (td.seconds % 3600) // 60
        final_hours = total_hours % 24
        return f"{final_hours:02}:{minutes:02}"
    
    @staticmethod
    def calc_time_difference_in_minutes(start_time, end_time):
        return (end_time - start_time).total_seconds() / 60
    
    def generate_duty_reports(self, include_trip=False):
        report = []
        for duty_id, duty_events in self.duties.items():
            start_times = []
            end_times = []
            trip_start_times = []
            trip_end_times = []

            for event in duty_events:
                vehicle_id = event.get('vehicle_id')
                vehicle_event_sequence = event.get('vehicle_event_sequence')
                if vehicle_id:
                    vehicle_events = self.vehicles.get(vehicle_id).get('vehicle_events')
                    v_event = {}
                    if vehicle_events:
                        for e in vehicle_events:
                            if int(e.get('vehicle_event_sequence')) == vehicle_event_sequence:
                                v_event = e
                                break

                    if v_event.get('vehicle_event_type') != 'service_trip':
                        start_times.append(self.parse_time(v_event.get('start_time')))
                        end_times.append(self.parse_time(v_event.get('end_time')))
                    else:
                        trip_id = v_event.get('trip_id')
                        trip = self.trips.get(trip_id)
                        if trip:
                            if include_trip:
                                trip_start_times.append([
                                    self.parse_time(trip.get('departure_time')),
                                    self.stops.get(trip.get('origin_stop_id', ''), {}).get('stop_name')
                                ])
                                trip_end_times.append([
                                    self.parse_time(trip.get('arrival_time')),
                                    self.stops.get(trip.get('destination_stop_id', ''), {}).get('stop_name')
                                ])
                            start_times.append(self.parse_time(trip.get('departure_time')))
                            end_times.append(self.parse_time(trip.get('arrival_time')))

            start_time = self.convert_timedelta_to_human_readable(min(start_times))
            end_time = self.convert_timedelta_to_human_readable(max(end_times))

            if include_trip:
                start_trip_time = min(trip_start_times, key=lambda x: x[0])[1]
                end_trip_time = max(trip_end_times, key=lambda x: x[0])[1]
                report.append([
                    duty_id, # Duty id
                    start_time, # Start time
                    end_time, # End time
                    start_trip_time, # Start stop description
                    end_trip_time # End stop description
                ])
                continue
            report.append([
                duty_id, # Duty id
                start_time, # Start time
                end_time, # End time
            ])
        return report

    def generate_duty_breaks_report(self):
        base_report = self.generate_duty_reports( include_trip=True)
        duty_dict = {}
        for row in base_report:
            duty_id = row[0]
            duty_dict[duty_id] = {}
            duty_dict[duty_id]['duty_id'] = duty_id
            duty_dict[duty_id]['start_time'] = row[1]
            duty_dict[duty_id]['end_time'] = row[2]
            duty_dict[duty_id]['start_trip'] = row[3]
            duty_dict[duty_id]['end_trip'] = row[4]

        valid_breaks = []

        for key, vehicle in self.vehicles.items():
            v_events = vehicle.get('vehicle_events', [])
            if len(v_events) > 0:
                # Because i need to check the difference between items, i should guarantee that the events are ordered.
                v_events = sorted(v_events, key=lambda x: int(x['vehicle_event_sequence']))
                for i in range(len(v_events) - 1):
                    current_event_end_time = 0
                    next_event_start_time = 0

                    current_event = v_events[i]
                    next_event = v_events[i+1]
                    break_stop_name = ''

                    if current_event.get('vehicle_event_type') == 'service_trip':
                        trip_id = current_event.get('trip_id')
                        trip = self.trips.get(trip_id)
                        if trip:
                            break_stop_name = self.stops.get(trip.get('destination_stop_id'), {}).get('stop_name')
                            self.stops.get(trip.get('origin_stop_id', ''), {}).get('stop_name')
                            if current_event.get('sub_trip_index'):
                                event_sub_trip_id = current_event.get('sub_trip_index')
                                sub_trips = trip.get('sub_trips')
                                sub_trip = {}
                                for s in sub_trips:
                                    if s.get('sub_trip_index') == f'{trip_id}_{event_sub_trip_id}':
                                        sub_trip = s
                                        break
                                current_event_end_time = self.parse_time(sub_trip.get('departure_time'))
                            else:
                                current_event_end_time = self.parse_time(trip.get('departure_time'))
                    else:
                        break_stop_name = self.stops.get(v_events[i].get('destination_stop_id'), {}).get('stop_name')
                        current_event_end_time = self.parse_time(v_events[i].get('end_time'))
                    
                    if next_event.get('vehicle_event_type') == 'service_trip':
                        trip_id = next_event.get('trip_id')
                        trip = self.trips.get(trip_id)
                        if trip:
                            if next_event.get('sub_trip_index'):
                                event_sub_trip_id = next_event.get('sub_trip_index')
                                sub_trips = trip.get('sub_trips')
                                sub_trip = {}
                                for s in sub_trips:
                                    if s.get('sub_trip_index') == f'{trip_id}_{event_sub_trip_id}':
                                        sub_trip = s
                                        break
                                next_event_start_time = self.parse_time(sub_trip.get('arrival_time'))
                            else:
                                next_event_start_time = self.parse_time(trip.get('arrival_time'))
                    else:
                        next_event_start_time = self.parse_time(v_events[i + 1].get('start_time'))

                    time_difference_in_minutes = self.calc_time_difference_in_minutes(current_event_end_time, next_event_start_time)
                    if time_difference_in_minutes > 15:
                        duty_info = duty_dict.get(current_event.get('duty_id'))
                        valid_breaks.append([
                            duty_info.get('duty_id'), # Duty id
                            duty_info.get('start_time'), # Start time
                            duty_info.get('end_time'), # End time
                            duty_info.get('start_trip'), # Start stop description
                            duty_info.get('end_trip'), # End stop description
                            self.convert_timedelta_to_human_readable(current_event_end_time), # Break start time
                            time_difference_in_minutes, # Break duration
                            break_stop_name # Break stop name
                        ])
        return valid_breaks
