require "json"
module Fixture_ordered_map_Crystal_json_type_json_any_ordered_map
extend self
my_data = JSON.parse(%({
    "name": "Alice",
    "age": 30,
    "active": true
}))
end
