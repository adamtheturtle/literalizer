require "json"
module Fixture_leading_zero_string_mapping_key_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%({
    "08": "value"
}))
end
