require "json"
module Fixture_string_with_dollar_brace_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%([
    "prefix ${HOME} suffix",
    "${interpolated}"
]))
end
