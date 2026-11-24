require "json"
module Fixture_literalize_ref_known_null_assignment_Crystal_json_type_json_any_ref_default
extend self
item = JSON.parse(%(null))
my_data = item
end
