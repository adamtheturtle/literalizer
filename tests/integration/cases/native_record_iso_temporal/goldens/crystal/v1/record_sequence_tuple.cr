module Fixture_native_record_iso_temporal_Crystal_record_sequence_tuple
extend self
record Record0, birthday : Time, moment : String, at : String
my_data = Record0.new(
    Time.utc(2024, 1, 15),
    "2024-01-15T12:30:00+00:00",
    "09:30:00",
)
end
