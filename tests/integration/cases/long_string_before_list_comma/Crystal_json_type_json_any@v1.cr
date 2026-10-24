require "json"
module Fixture_long_string_before_list_comma_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%([
    "This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.",
    1
]))
end
