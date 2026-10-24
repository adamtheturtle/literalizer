require "json"
module Fixture_zig_delete_string_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%({
    "v": "ab",
    "ab": 1
}))
end
