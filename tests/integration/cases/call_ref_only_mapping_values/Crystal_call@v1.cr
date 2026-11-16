module Fixture_call_ref_only_mapping_values_Crystal_call
extend self
def consume(value = nil); 0; end
item = 42
consume(value: {"field" => item});
end
