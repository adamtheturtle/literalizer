require "json"
module Fixture_ragged_map_sequence_values_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%({
    "a": [{"item": [1]}],
    "b": [{"item": [2, 3]}]
}))
end
