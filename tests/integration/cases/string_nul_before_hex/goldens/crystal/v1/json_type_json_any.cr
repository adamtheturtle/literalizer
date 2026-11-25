require "json"
module Fixture_string_nul_before_hex_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%({
    "x": "before\\u0000after"
}))
end
