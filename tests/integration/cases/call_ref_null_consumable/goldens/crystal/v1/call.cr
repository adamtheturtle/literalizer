module Fixture_call_ref_null_consumable_Crystal_call
extend self
def consume(value = nil); 0; end
my_null = nil
regular_null = nil
consume(value: my_null);
consume(value: regular_null);
end
