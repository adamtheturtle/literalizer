require "json"
module Fixture_call_csharp_json_repeated_scalar_Crystal_json_type_json_any_call
extend self
def consume(value = nil); 0; end
shared = JSON.parse(%(42))
consume(value: JSON.parse(%([shared, shared])));
end
