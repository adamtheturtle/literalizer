require "json"
module Fixture_string_carriage_return_line_feed_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%({
    "cr": "a\\rb",
    "crlf": "a\\r\\nb",
    "lf": "a\\nb"
}))
end
