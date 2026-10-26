require "json"
module Fixture_widened_i64_minimum_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%([
    -9223372036854775808,
    5
]))
end
