require "json"
module Fixture_empty_key_is_data_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%([
    {"": "external_value"}
]))
end
