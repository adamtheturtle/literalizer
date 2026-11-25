require "json"
module Fixture_dates_Crystal_json_type_json_any_dates
extend self
my_data = JSON.parse(%({
    "date": "2024-01-15",
    "datetime": "2024-01-15T12:30:00+00:00"
}))
end
