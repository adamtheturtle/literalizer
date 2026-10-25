require "json"
module Fixture_nested_empty_inner_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%([
    [],
    []
]))
end
