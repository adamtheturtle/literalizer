require "json"
module Fixture_four_dimensional_empty_lists_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%([
    [[[]]],
    [[[]]]
]))
end
