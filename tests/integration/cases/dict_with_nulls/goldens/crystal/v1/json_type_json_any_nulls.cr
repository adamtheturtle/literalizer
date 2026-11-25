require "json"
module Fixture_dict_with_nulls_Crystal_json_type_json_any_nulls
extend self
my_data = JSON.parse(%({
    "name": "Alice",
    "score": null,
    "age": 30
}))
end
