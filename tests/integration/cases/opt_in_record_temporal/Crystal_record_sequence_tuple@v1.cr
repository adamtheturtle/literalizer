module Fixture_opt_in_record_temporal_Crystal_record_sequence_tuple
extend self
record Record0, event_date : Time, event_time : String, event_datetime : String
my_data = Record0.new(
    Time.utc(2024, 1, 15),
    "12:30:00",
    "2024-01-15T12:30:00+00:00",
)
end
