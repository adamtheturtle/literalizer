require "json"
module Fixture_literalize_ref_value_type_hint_Crystal_json_type_json_any_ref
extend self
ref_data = JSON.parse(%([
    1,
    2
]))
my_data = ref_data
end
