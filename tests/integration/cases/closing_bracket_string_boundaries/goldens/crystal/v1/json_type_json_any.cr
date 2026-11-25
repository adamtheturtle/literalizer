require "json"
module Fixture_closing_bracket_string_boundaries_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%([
    "]",
    "a]",
    "a]=",
    "a]b"
]))
end
