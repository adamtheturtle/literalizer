require "json"
module Fixture_scalar_time_microsecond_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%({
    "exact_millisecond": "09:30:15.123000",
    "sub_millisecond": "09:30:15.123456"
}))
end
