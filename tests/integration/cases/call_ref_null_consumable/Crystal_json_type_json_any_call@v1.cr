require "json"
module Fixture_call_ref_null_consumable_Crystal_json_type_json_any_call
extend self
def consume(value = nil); 0; end
my_null = JSON.parse(%(null))
regular_null = JSON.parse(%(null))
consume(value: my_null);
consume(value: regular_null);
end
