require "json"
module Fixture_nested_mixed_inner_Crystal_json_type_json_any_nested_mixed
extend self
my_data = JSON.parse(%([
    [1, "a"],
    [2, "b"]
]))
end
