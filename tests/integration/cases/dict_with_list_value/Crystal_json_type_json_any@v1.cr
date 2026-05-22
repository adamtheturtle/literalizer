require "json"
module Fixture_dict_with_list_value_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%({
    "name": "Alice",
    "scores": [10, 20, 30]
}))
end
