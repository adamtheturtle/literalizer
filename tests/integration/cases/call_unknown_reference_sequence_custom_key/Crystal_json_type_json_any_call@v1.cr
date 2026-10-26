require "json"
module Fixture_call_unknown_reference_sequence_custom_key_Crystal_json_type_json_any_call
extend self
def process(data = nil); 0; end
untyped_value = JSON.parse(%([]))
process(data: JSON.parse(%([#{untyped_value.to_json}, #{untyped_value.to_json}])));
end
