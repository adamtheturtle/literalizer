require "json"
module Fixture_time_list_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%({
    "times": ["09:30:00", "17:45:00", "23:59:59"]
}))
end
