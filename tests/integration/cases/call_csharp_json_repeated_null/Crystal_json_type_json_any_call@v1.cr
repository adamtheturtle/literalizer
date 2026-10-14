require "json"
module Fixture_call_csharp_json_repeated_null_Crystal_json_type_json_any_call
extend self
def consume(value = nil); 0; end
shared = JSON.parse(%(null))
consume(value: JSON.parse(%({"left": shared, "nested": [shared]})));
end
