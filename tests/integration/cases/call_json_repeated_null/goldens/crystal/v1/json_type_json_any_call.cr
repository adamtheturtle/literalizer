require "json"
module Fixture_call_json_repeated_null_Crystal_json_type_json_any_call
extend self
def consume(value = nil); 0; end
shared = JSON.parse(%(null))
consume(value: JSON.parse(%({"left": #{shared.to_json}, "nested": [#{shared.to_json}]})));
end
