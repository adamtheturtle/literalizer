require "json"
module Fixture_epoch_datetime_map_values_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%({
    "within_i32": "2024-01-15T12:00:00",
    "beyond_i32": "2099-06-15T08:30:00"
}))
end
