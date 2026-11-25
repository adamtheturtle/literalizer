require "json"
module Fixture_ordered_map_proto_key_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%({
    "__proto__": {"x": 1},
    "ordinary": 2
}))
end
