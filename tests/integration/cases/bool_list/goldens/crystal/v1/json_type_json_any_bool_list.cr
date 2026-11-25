require "json"
module Fixture_bool_list_Crystal_json_type_json_any_bool_list
extend self
my_data = JSON.parse(%([
    true,
    false,
    true
]))
end
