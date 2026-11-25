require "json"
module Fixture_multiline_string_scalar_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%("\\nroot first line\\n  indented\\n\\nroot last line\\n"))
end
