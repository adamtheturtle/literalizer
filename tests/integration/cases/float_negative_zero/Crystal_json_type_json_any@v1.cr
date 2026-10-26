require "json"
module Fixture_float_negative_zero_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%([
    -0.0,
    1.5
]))
end
