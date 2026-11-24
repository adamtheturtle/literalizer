require "json"
module Fixture_call_json_nested_ref_array_Crystal_json_type_json_any_call
extend self
def consume(value = nil); 0; end
shared = JSON.parse(%([
    1,
    2
]))
consume(value: JSON.parse(%([#{shared.to_json}, 42])));
end
