require "json"
module Fixture_multiline_string_nested_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%({
    "outer": [["nested first line\\n  indented\\n\\nnested last line\\n"]]
}))
end
