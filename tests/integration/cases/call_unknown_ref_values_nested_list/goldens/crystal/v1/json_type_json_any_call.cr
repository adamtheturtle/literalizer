require "json"
module Fixture_call_unknown_ref_values_nested_list_Crystal_json_type_json_any_call
extend self
def process(data = nil); 0; end
unknown_value = JSON.parse(%([]))
process(data: JSON.parse(%([#{unknown_value.to_json}])));
end
