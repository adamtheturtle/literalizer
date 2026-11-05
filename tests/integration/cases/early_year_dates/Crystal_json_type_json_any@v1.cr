require "json"
module Fixture_early_year_dates_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%({
    "date": "0099-05-27",
    "naive": "0001-01-01T12:30:00",
    "recent": "2024-05-27T10:00:00"
}))
end
