require "json"
module Fixture_sibling_list_values_same_shape_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%({
    "test": [5, ["compile", "test"]],
    "package": [7, ["link", "test"]]
}))
end
