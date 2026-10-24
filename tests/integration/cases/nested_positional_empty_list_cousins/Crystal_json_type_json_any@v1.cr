require "json"
module Fixture_nested_positional_empty_list_cousins_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%([
    [[], []],
    [[1], [1]]
]))
end
