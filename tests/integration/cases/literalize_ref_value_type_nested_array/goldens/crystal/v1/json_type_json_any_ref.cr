require "json"
module Fixture_literalize_ref_value_type_nested_array_Crystal_json_type_json_any_ref
extend self
shared = JSON.parse(%([
    1,
    2
]))
my_data = JSON.parse(%([
    #{shared.to_json},
    42
]))
end
