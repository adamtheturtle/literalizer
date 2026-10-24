require "json"
module Fixture_dict_proto_key_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%({
    "__proto__": {"x": 1},
    "n": {"__proto__": 3},
    "y": 2
}))
end
