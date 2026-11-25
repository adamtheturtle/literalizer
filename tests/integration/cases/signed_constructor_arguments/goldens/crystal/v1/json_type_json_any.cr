require "json"
module Fixture_signed_constructor_arguments_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%([
    -42,
    0,
    42,
    -1.25,
    0.0,
    1.25
]))
end
