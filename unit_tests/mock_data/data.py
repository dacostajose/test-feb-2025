sample_mock = {
    "stops": [
        {"stop_id": "1", "stop_name": "Stop A"},
        {"stop_id": "2", "stop_name": "Stop B"}
    ],
    "trips": [
        {"trip_id": "1", "origin_stop_id": "1", "destination_stop_id": "2", "departure_time": "0.08:00", "arrival_time": "0.09:00"}
    ],
    "vehicles": [
        {
            "vehicle_id": "1",
            "vehicle_events": [
                {"vehicle_event_sequence": "1", "vehicle_event_type": "service", "start_time": "0.07:00", "end_time": "0.08:00"},
                {"vehicle_event_sequence": "2", "vehicle_event_type": "service_trip", "trip_id": "1", "start_time": "0.08:00", "end_time": "0.09:00"}
            ]
        }
    ],
    "duties": [
        {
            "duty_id": "1",
            "duty_events": [
                {"vehicle_id": "1", "vehicle_event_sequence": 1},
                {"vehicle_id": "1", "vehicle_event_sequence": 2}
            ]
        }
    ]
}