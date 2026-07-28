module Fixture_call_unknown_ref_nested_Crystal_call
extend self
def process(known_value = nil, nested_missing = nil); 0; end
known_value = true
unknown_value = true
process(known_value: known_value, nested_missing: [unknown_value]);
end
