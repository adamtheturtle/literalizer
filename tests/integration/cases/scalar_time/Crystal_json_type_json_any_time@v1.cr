require "json"
module Fixture_scalar_time_Crystal_json_type_json_any_time
extend self
my_data = JSON.parse(%({
    "starts_at": "09:30:00"
}))
end
