require "json"
module Fixture_multiline_string_nested_list_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%([
    ["\\nfirst line\\n  indented\\n\\nlast line\\n"]
]))
end
