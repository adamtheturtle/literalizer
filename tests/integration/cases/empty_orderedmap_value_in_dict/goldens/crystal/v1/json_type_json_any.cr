require "json"
module Fixture_empty_orderedmap_value_in_dict_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%({
    "a": {},
    "b": 1
}))
end
