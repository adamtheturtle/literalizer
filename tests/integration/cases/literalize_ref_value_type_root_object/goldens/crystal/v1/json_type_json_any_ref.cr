require "json"
module Fixture_literalize_ref_value_type_root_object_Crystal_json_type_json_any_ref
extend self
shared = JSON.parse(%({
    "field": [1, 2]
}))
my_data = shared
end
