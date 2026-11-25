require "json"
module Fixture_negative_zero_constructor_arguments_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%([
    -0.0,
    0.0
]))
end
