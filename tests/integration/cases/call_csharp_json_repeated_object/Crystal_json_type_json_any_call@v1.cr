require "json"
module Fixture_call_csharp_json_repeated_object_Crystal_json_type_json_any_call
extend self
def consume(value = nil); 0; end
shared = JSON.parse(%({
    "value": [1, 2]
}))
consume(value: JSON.parse(%({"left": shared, "right": shared})));
end
