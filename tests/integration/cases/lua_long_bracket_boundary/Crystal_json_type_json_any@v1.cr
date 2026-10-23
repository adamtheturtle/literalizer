require "json"
module Fixture_lua_long_bracket_boundary_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%([
    "]",
    "a]",
    "a]=",
    "a]b"
]))
end
