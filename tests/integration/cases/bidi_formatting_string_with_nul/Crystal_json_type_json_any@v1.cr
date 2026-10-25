require "json"
module Fixture_bidi_formatting_string_with_nul_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%({
    "v": "a‪\\u0000é😀b"
}))
end
