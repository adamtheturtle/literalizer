require "json"
module Fixture_time_dict_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%({
    "morning": "09:30:00",
    "afternoon": "14:15:00",
    "evening": "23:59:59"
}))
end
