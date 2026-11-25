require "json"
module Fixture_literalize_ref_repeated_value_type_Crystal_json_type_json_any_ref
extend self
shared = JSON.parse(%(42))
my_data = JSON.parse(%([
    #{shared.to_json},
    #{shared.to_json}
]))
end
