require "json"
module Fixture_binary_with_empty_sibling_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%([
    "48656c6c6f",
    []
]))
end
